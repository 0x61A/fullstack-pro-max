#!/usr/bin/env python3
"""Scaffold a queue-friendly transactional email module for a provider.

Stdlib only -- no third-party dependencies (references/conventions.md). The
*generated* code uses the project's own installed provider SDK (resend,
postmark, or the AWS SDK).

Every scaffold bakes in this module's sending non-negotiables: suppression
check before dispatch (EM013/EM027), an idempotency key (EM012), env-based
API keys (EM032), and a sandbox guard so non-production environments can't
send real mail (EM010).

Examples:
    python3 generate.py --provider resend --stack node --dry-run
    python3 generate.py --provider ses --stack python --output src/lib/
"""

import argparse
from pathlib import Path

NODE_CLIENTS = {
    "resend": (
        '// Requires: npm install resend\nimport { Resend } from "resend";\nconst client = new Resend(process.env.RESEND_API_KEY);',
        'const { error } = await client.emails.send({ from: FROM, to: msg.to, subject: msg.subject, html: msg.html, text: msg.text });\n  if (error) throw new Error(error.message);',
    ),
    "postmark": (
        '// Requires: npm install postmark\nimport { ServerClient } from "postmark";\nconst client = new ServerClient(process.env.POSTMARK_SERVER_TOKEN!);',
        'await client.sendEmail({ From: FROM, To: msg.to, Subject: msg.subject, HtmlBody: msg.html, TextBody: msg.text, MessageStream: "outbound" });',
    ),
    "ses": (
        '// Requires: npm install @aws-sdk/client-sesv2\nimport { SESv2Client, SendEmailCommand } from "@aws-sdk/client-sesv2";\nconst client = new SESv2Client({});',
        'await client.send(new SendEmailCommand({ FromEmailAddress: FROM, Destination: { ToAddresses: [msg.to] }, Content: { Simple: { Subject: { Data: msg.subject }, Body: { Html: { Data: msg.html }, Text: { Data: msg.text } } } } }));',
    ),
}

NODE_TEMPLATE = '''// lib/email.ts -- transactional email sender ({provider}).
// Env keys only (EM032); see references/email-integration.md.
{client_init}

const FROM = process.env.EMAIL_FROM ?? "Product <mail@yourdomain.com>"; // aligned sending domain (EM019/EM024)

type Message = {{
  to: string;
  subject: string;
  html: string;
  text: string;          // always ship a real plain-text part (EM017)
  idempotencyKey: string; // e.g. `${{orderId}}:receipt` (EM012)
}};

// TODO: back these two with your DB (suppression table + sent-log table).
async function isSuppressed(to: string): Promise<boolean> {{ return false; }}   // EM013/EM027
async function alreadySent(key: string): Promise<boolean> {{ return false; }}   // EM012
async function markSent(key: string): Promise<void> {{}}

export async function sendEmail(msg: Message): Promise<void> {{
  // EM010: non-production must never deliver real mail -- point at Mailpit/
  // sandbox via env, or log-and-return here.
  if (process.env.NODE_ENV !== "production" && !process.env.EMAIL_SANDBOX_HOST) {{
    console.log("[email:dry]", msg.to, msg.subject);
    return;
  }}
  if (await isSuppressed(msg.to)) return;        // never mail the suppressed (EM027)
  if (await alreadySent(msg.idempotencyKey)) return;

  {send_call}

  await markSent(msg.idempotencyKey);
}}

// Call this from a queue worker (EM011), not from the request path:
// the HTTP handler enqueues {{to, subject, ...}}, the worker calls sendEmail.
'''

PYTHON_CLIENTS = {
    "resend": (
        '# Requires: pip install resend\nimport resend\n\nresend.api_key = os.environ["RESEND_API_KEY"]',
        'resend.Emails.send({"from": FROM, "to": msg.to, "subject": msg.subject, "html": msg.html, "text": msg.text})',
    ),
    "postmark": (
        '# Requires: pip install postmarker\nfrom postmarker.core import PostmarkClient\n\nclient = PostmarkClient(server_token=os.environ["POSTMARK_SERVER_TOKEN"])',
        'client.emails.send(From=FROM, To=msg.to, Subject=msg.subject, HtmlBody=msg.html, TextBody=msg.text, MessageStream="outbound")',
    ),
    "ses": (
        '# Requires: pip install boto3\nimport boto3\n\nclient = boto3.client("sesv2")',
        'client.send_email(FromEmailAddress=FROM, Destination={"ToAddresses": [msg.to]}, Content={"Simple": {"Subject": {"Data": msg.subject}, "Body": {"Html": {"Data": msg.html}, "Text": {"Data": msg.text}}}})',
    ),
}

PYTHON_TEMPLATE = '''# lib/email.py -- transactional email sender ({provider}).
# Env keys only (EM032); see references/email-integration.md.
import os
from dataclasses import dataclass

{client_init}

FROM = os.environ.get("EMAIL_FROM", "Product <mail@yourdomain.com>")  # aligned sending domain (EM019/EM024)


@dataclass
class Message:
    to: str
    subject: str
    html: str
    text: str             # always ship a real plain-text part (EM017)
    idempotency_key: str  # e.g. f"{{order_id}}:receipt" (EM012)


# TODO: back these with your DB (suppression table + sent-log table).
def is_suppressed(to: str) -> bool:  # EM013/EM027
    return False


def already_sent(key: str) -> bool:  # EM012
    return False


def mark_sent(key: str) -> None:
    pass


def send_email(msg: Message) -> None:
    # EM010: non-production must never deliver real mail.
    if os.environ.get("APP_ENV", "development") != "production" and not os.environ.get("EMAIL_SANDBOX_HOST"):
        print(f"[email:dry] {{msg.to}} {{msg.subject}}")
        return
    if is_suppressed(msg.to):   # never mail the suppressed (EM027)
        return
    if already_sent(msg.idempotency_key):
        return

    {send_call}

    mark_sent(msg.idempotency_key)


# Call from a queue worker (EM011), not the request path: the endpoint
# enqueues the message, the worker calls send_email.
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--provider", required=True, choices=sorted(NODE_CLIENTS))
    parser.add_argument("--stack", required=True, choices=["node", "python"])
    parser.add_argument("--output", default="generated", help="Output directory (default: generated/)")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be written instead of writing it")
    args = parser.parse_args()

    if args.stack == "node":
        client_init, send_call = NODE_CLIENTS[args.provider]
        content = NODE_TEMPLATE.format(provider=args.provider, client_init=client_init, send_call=send_call)
        rel_path = "lib/email.ts"
    else:
        client_init, send_call = PYTHON_CLIENTS[args.provider]
        content = PYTHON_TEMPLATE.format(provider=args.provider, client_init=client_init, send_call=send_call)
        rel_path = "lib/email.py"

    out_path = Path(args.output) / rel_path
    if args.dry_run:
        print(f"--- would write {out_path} ---")
        print(content)
        return

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(f"wrote {out_path}")
    print("Next: wire the suppression/idempotency TODOs to your DB, then run the deliverability checklist (data/email/deliverability-checklist.csv).")


if __name__ == "__main__":
    main()
