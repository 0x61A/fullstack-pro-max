#!/usr/bin/env python3
"""Scaffold a signature-verified, idempotent webhook handler for Stripe or Shopify.

Stdlib only -- no third-party dependencies (references/conventions.md).
Every generated handler verifies the provider's signature before trusting
the payload (EC006/EC022), includes an idempotency-check stub keyed on the
event id (EC007/EC023), and responds fast while leaving slow work as an
explicit TODO to move to a queue (EC008) -- the three non-negotiables from
stripe-integration.md / shopify-integration.md.

Examples:
    python3 generate.py --provider stripe --stack nextjs-api --output ./my-app
    python3 generate.py --provider shopify --stack express --output ./my-app
    python3 generate.py --provider stripe --stack fastapi --output ./my-app --dry-run
"""

import argparse
from pathlib import Path

PROVIDERS = ["stripe", "shopify"]
STACKS = ["nextjs-api", "express", "fastapi"]


def render_nextjs(provider: str) -> str:
    if provider == "stripe":
        return """import { NextRequest, NextResponse } from "next/server";
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!;

// TODO: replace with a real store (Redis/DB) -- this in-memory Set resets on
// every cold start and does NOT provide real idempotency across instances.
const processedEventIds = new Set<string>();

export async function POST(request: NextRequest) {
  const signature = request.headers.get("stripe-signature");
  const body = await request.text();

  let event: Stripe.Event;
  try {
    // Signature verification (EC006) -- never trust the payload before this passes.
    event = stripe.webhooks.constructEvent(body, signature!, webhookSecret);
  } catch (err) {
    console.error("Webhook signature verification failed", err);
    return NextResponse.json({ error: { code: "invalid_signature" } }, { status: 400 });
  }

  // Idempotency (EC007) -- Stripe may redeliver the same event.
  if (processedEventIds.has(event.id)) {
    return NextResponse.json({ received: true, deduped: true });
  }
  processedEventIds.add(event.id);

  switch (event.type) {
    case "payment_intent.succeeded":
      // TODO: fulfill the order. If this is slow, enqueue it (EC008) --
      // respond fast and do slow work asynchronously.
      break;
    case "charge.dispute.created":
      // TODO: alert a human -- dispute deadlines are real (EC012).
      break;
    default:
      // TODO: handle additional event types as needed.
      break;
  }

  return NextResponse.json({ received: true });
}
"""
    return """import { NextRequest, NextResponse } from "next/server";
import crypto from "crypto";

const webhookSecret = process.env.SHOPIFY_WEBHOOK_SECRET!;
const processedEventIds = new Set<string>(); // TODO: replace with a real store

function verifyShopifyHmac(rawBody: string, hmacHeader: string | null): boolean {
  if (!hmacHeader) return false;
  const digest = crypto.createHmac("sha256", webhookSecret).update(rawBody, "utf8").digest("base64");
  // Constant-time comparison to avoid timing attacks.
  return crypto.timingSafeEqual(Buffer.from(digest), Buffer.from(hmacHeader));
}

export async function POST(request: NextRequest) {
  const hmacHeader = request.headers.get("x-shopify-hmac-sha256");
  const body = await request.text();

  // Signature verification (EC022) -- never trust the payload before this passes.
  if (!verifyShopifyHmac(body, hmacHeader)) {
    console.error("Shopify webhook signature verification failed");
    return NextResponse.json({ error: { code: "invalid_signature" } }, { status: 401 });
  }

  const topic = request.headers.get("x-shopify-topic") ?? "unknown";
  const eventId = request.headers.get("x-shopify-webhook-id") ?? "";

  // Idempotency (EC023) -- Shopify may redeliver the same webhook.
  if (eventId && processedEventIds.has(eventId)) {
    return NextResponse.json({ received: true, deduped: true });
  }
  if (eventId) processedEventIds.add(eventId);

  const payload = JSON.parse(body);

  switch (topic) {
    case "orders/create":
      // TODO: sync the order. If this is slow, enqueue it (EC008).
      break;
    case "inventory_levels/update":
      // TODO: sync inventory -- Shopify is the source of truth (EC025).
      break;
    default:
      // TODO: handle additional topics as needed.
      break;
  }

  return NextResponse.json({ received: true });
}
"""


def render_express(provider: str) -> str:
    if provider == "stripe":
        return """const Stripe = require("stripe");
const stripe = Stripe(process.env.STRIPE_SECRET_KEY);
const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

// TODO: replace with a real store (Redis/DB) -- resets on restart.
const processedEventIds = new Set();

// NOTE: this route must receive the RAW request body (not JSON-parsed) for
// signature verification to work -- register with express.raw({ type: "application/json" }).
function stripeWebhookHandler(req, res) {
  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, req.headers["stripe-signature"], webhookSecret);
  } catch (err) {
    console.error("Webhook signature verification failed", err);
    return res.status(400).json({ error: { code: "invalid_signature" } });
  }

  if (processedEventIds.has(event.id)) {
    return res.json({ received: true, deduped: true });
  }
  processedEventIds.add(event.id);

  switch (event.type) {
    case "payment_intent.succeeded":
      // TODO: fulfill the order. If slow, enqueue it (EC008).
      break;
    case "charge.dispute.created":
      // TODO: alert a human -- dispute deadlines are real (EC012).
      break;
    default:
      break;
  }

  res.json({ received: true });
}

module.exports = { stripeWebhookHandler };
"""
    return """const crypto = require("crypto");
const webhookSecret = process.env.SHOPIFY_WEBHOOK_SECRET;
const processedEventIds = new Set(); // TODO: replace with a real store

function verifyShopifyHmac(rawBody, hmacHeader) {
  if (!hmacHeader) return false;
  const digest = crypto.createHmac("sha256", webhookSecret).update(rawBody, "utf8").digest("base64");
  return crypto.timingSafeEqual(Buffer.from(digest), Buffer.from(hmacHeader));
}

// NOTE: this route must receive the RAW request body for HMAC verification
// to work -- register with express.raw({ type: "application/json" }).
function shopifyWebhookHandler(req, res) {
  const hmacHeader = req.headers["x-shopify-hmac-sha256"];

  if (!verifyShopifyHmac(req.body, hmacHeader)) {
    console.error("Shopify webhook signature verification failed");
    return res.status(401).json({ error: { code: "invalid_signature" } });
  }

  const topic = req.headers["x-shopify-topic"] || "unknown";
  const eventId = req.headers["x-shopify-webhook-id"] || "";

  if (eventId && processedEventIds.has(eventId)) {
    return res.json({ received: true, deduped: true });
  }
  if (eventId) processedEventIds.add(eventId);

  const payload = JSON.parse(req.body.toString("utf8"));

  switch (topic) {
    case "orders/create":
      // TODO: sync the order. If slow, enqueue it (EC008).
      break;
    case "inventory_levels/update":
      // TODO: sync inventory -- Shopify is the source of truth (EC025).
      break;
    default:
      break;
  }

  res.json({ received: true });
}

module.exports = { shopifyWebhookHandler };
"""


def render_fastapi(provider: str) -> str:
    if provider == "stripe":
        return '''"""Stripe webhook handler -- signature-verified (EC006), idempotent (EC007)."""

import os
import stripe
from fastapi import APIRouter, Request, HTTPException

router = APIRouter()
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
webhook_secret = os.environ["STRIPE_WEBHOOK_SECRET"]

# TODO: replace with a real store (Redis/DB) -- resets on restart.
processed_event_ids: set[str] = set()


@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(payload, signature, webhook_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(status_code=400, detail="invalid_signature")

    if event["id"] in processed_event_ids:
        return {"received": True, "deduped": True}
    processed_event_ids.add(event["id"])

    event_type = event["type"]
    if event_type == "payment_intent.succeeded":
        pass  # TODO: fulfill the order. If slow, enqueue it (EC008).
    elif event_type == "charge.dispute.created":
        pass  # TODO: alert a human -- dispute deadlines are real (EC012).

    return {"received": True}
'''
    return '''"""Shopify webhook handler -- HMAC-verified (EC022), idempotent (EC023)."""

import base64
import hashlib
import hmac
import json
import os
from fastapi import APIRouter, Request, HTTPException

router = APIRouter()
webhook_secret = os.environ["SHOPIFY_WEBHOOK_SECRET"].encode("utf-8")

# TODO: replace with a real store (Redis/DB) -- resets on restart.
processed_event_ids: set[str] = set()


def verify_shopify_hmac(raw_body: bytes, hmac_header: str) -> bool:
    digest = hmac.new(webhook_secret, raw_body, hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode("utf-8")
    return hmac.compare_digest(expected, hmac_header)


@router.post("/webhooks/shopify")
async def shopify_webhook(request: Request):
    raw_body = await request.body()
    hmac_header = request.headers.get("x-shopify-hmac-sha256", "")

    if not verify_shopify_hmac(raw_body, hmac_header):
        raise HTTPException(status_code=401, detail="invalid_signature")

    topic = request.headers.get("x-shopify-topic", "unknown")
    event_id = request.headers.get("x-shopify-webhook-id", "")

    if event_id and event_id in processed_event_ids:
        return {"received": True, "deduped": True}
    if event_id:
        processed_event_ids.add(event_id)

    payload = json.loads(raw_body)

    if topic == "orders/create":
        pass  # TODO: sync the order. If slow, enqueue it (EC008).
    elif topic == "inventory_levels/update":
        pass  # TODO: sync inventory -- Shopify is the source of truth (EC025).

    return {"received": True}
'''


RENDERERS = {"nextjs-api": render_nextjs, "express": render_express, "fastapi": render_fastapi}
FILE_PATHS = {
    "nextjs-api": {"stripe": "app/api/webhooks/stripe/route.ts", "shopify": "app/api/webhooks/shopify/route.ts"},
    "express": {"stripe": "src/webhooks/stripe.js", "shopify": "src/webhooks/shopify.js"},
    "fastapi": {"stripe": "app/webhooks/stripe.py", "shopify": "app/webhooks/shopify.py"},
}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--provider", required=True, choices=PROVIDERS)
    parser.add_argument("--stack", required=True, choices=STACKS)
    parser.add_argument("--output", type=Path, default=Path("./generated"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    content = RENDERERS[args.stack](args.provider)
    target = args.output / FILE_PATHS[args.stack][args.provider]

    if args.dry_run:
        print(f"--- would write {target} ---")
        print(content)
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    print(f"wrote {target}")
    print("Replace the in-memory idempotency Set with a real store (Redis/DB) before production use.")
    if args.stack == "express":
        print("Register this route with express.raw({ type: 'application/json' }) -- signature verification needs the raw body.")


if __name__ == "__main__":
    main()
