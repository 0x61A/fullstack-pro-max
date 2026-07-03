#!/usr/bin/env python3
"""Scaffold a CRUD API endpoint for a resource, in the stack of your choice.

Stdlib only -- no third-party dependencies, per this skill's conventions
(references/conventions.md). Generated code follows the patterns documented
in references/backend-architecture.md and references/api-design.md:
validation at the boundary (BE080), a consistent error envelope (BE082),
and the controller/service split where the stack doesn't impose one itself.

This writes idiomatic starting-point code, not a finished feature -- fill in
real validation schemas, persistence calls, and auth checks before shipping.

Examples:
    python3 generate.py todo --stack nextjs-api --output ./my-app
    python3 generate.py order-item --stack fastapi --output ./my-app --dry-run
    python3 generate.py invoice --stack supabase-edge --output ./my-app
"""

import argparse
import re
import sys
from pathlib import Path

STACKS = ["nextjs-api", "express", "nestjs", "fastapi", "django", "supabase-edge"]


# ---------------------------------------------------------------------------
# Naming helpers
# ---------------------------------------------------------------------------

def split_words(name: str):
    name = re.sub(r"[_\-\s]+", " ", name).strip()
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name)
    return [w.lower() for w in name.split(" ") if w]


def naive_plural(word: str) -> str:
    if word.endswith(("s", "x", "ch", "sh")):
        return word + "es"
    if word.endswith("y") and word[-2:-1] not in "aeiou":
        return word[:-1] + "ies"
    return word + "s"


class Names:
    def __init__(self, raw: str):
        words = split_words(raw)
        if not words:
            raise ValueError("resource name must contain at least one word")
        self.words = words
        self.kebab = "-".join(words)
        self.snake = "_".join(words)
        self.camel = words[0] + "".join(w.capitalize() for w in words[1:])
        self.pascal = "".join(w.capitalize() for w in words)
        plural_words = words[:-1] + [naive_plural(words[-1])]
        self.kebab_plural = "-".join(plural_words)
        self.snake_plural = "_".join(plural_words)
        self.camel_plural = plural_words[0] + "".join(w.capitalize() for w in plural_words[1:])


# ---------------------------------------------------------------------------
# Templates -- each returns a list of (relative_path, content) tuples
# ---------------------------------------------------------------------------

def tpl_nextjs_api(n: Names):
    collection = f"""import {{ NextRequest, NextResponse }} from "next/server";
// import {{ {n.pascal}Schema }} from "@/lib/validation/{n.kebab}";

// GET /api/{n.kebab_plural} -- list {n.camel_plural}
export async function GET(request: NextRequest) {{
  try {{
    // TODO: read + validate query params (pagination, filters) -- see BE080
    const {n.camel_plural} = await find{n.pascal}s();
    return NextResponse.json({{ data: {n.camel_plural} }});
  }} catch (err) {{
    return errorResponse(err);
  }}
}}

// POST /api/{n.kebab_plural} -- create a new {n.camel}
export async function POST(request: NextRequest) {{
  try {{
    const body = await request.json();
    // const parsed = {n.pascal}Schema.parse(body); // validate at the boundary, BE080
    const created = await create{n.pascal}(body);
    return NextResponse.json({{ data: created }}, {{ status: 201 }});
  }} catch (err) {{
    return errorResponse(err);
  }}
}}

// Replace with real persistence -- these are placeholders so the route compiles.
async function find{n.pascal}s() {{
  return [];
}}
async function create{n.pascal}(input: unknown) {{
  return input;
}}

// Consistent error envelope, see references/api-design.md and BE082.
function errorResponse(err: unknown) {{
  console.error(err);
  return NextResponse.json(
    {{ error: {{ code: "internal_error", message: "Something went wrong" }} }},
    {{ status: 500 }}
  );
}}
"""
    item = f"""import {{ NextRequest, NextResponse }} from "next/server";

// GET /api/{n.kebab_plural}/[id]
export async function GET(request: NextRequest, {{ params }}: {{ params: {{ id: string }} }}) {{
  const {n.camel} = await find{n.pascal}ById(params.id);
  if (!{n.camel}) {{
    return NextResponse.json(
      {{ error: {{ code: "not_found", message: "{n.pascal} not found" }} }},
      {{ status: 404 }}
    );
  }}
  return NextResponse.json({{ data: {n.camel} }});
}}

// PATCH /api/{n.kebab_plural}/[id]
export async function PATCH(request: NextRequest, {{ params }}: {{ params: {{ id: string }} }}) {{
  const body = await request.json();
  // TODO: validate `body` at the boundary (BE080) before applying it
  const updated = await update{n.pascal}(params.id, body);
  return NextResponse.json({{ data: updated }});
}}

// DELETE /api/{n.kebab_plural}/[id]
export async function DELETE(request: NextRequest, {{ params }}: {{ params: {{ id: string }} }}) {{
  await delete{n.pascal}(params.id);
  return new NextResponse(null, {{ status: 204 }});
}}

async function find{n.pascal}ById(id: string) {{
  return null;
}}
async function update{n.pascal}(id: string, input: unknown) {{
  return input;
}}
async function delete{n.pascal}(id: string) {{
  return;
}}
"""
    return [
        (f"app/api/{n.kebab_plural}/route.ts", collection),
        (f"app/api/{n.kebab_plural}/[id]/route.ts", item),
    ]


def tpl_express(n: Names):
    routes = f"""import {{ Router }} from "express";
import * as controller from "./{n.kebab}.controller";

const router = Router();

router.get("/{n.kebab_plural}", controller.list{n.pascal}s);
router.post("/{n.kebab_plural}", controller.create{n.pascal});
router.get("/{n.kebab_plural}/:id", controller.get{n.pascal});
router.patch("/{n.kebab_plural}/:id", controller.update{n.pascal});
router.delete("/{n.kebab_plural}/:id", controller.delete{n.pascal});

export default router;
"""
    controller = f"""import {{ Request, Response, NextFunction }} from "express";
import * as service from "./{n.kebab}.service";
// import {{ {n.pascal}Schema }} from "../validation/{n.kebab}"; // BE080

export async function list{n.pascal}s(req: Request, res: Response, next: NextFunction) {{
  try {{
    const {n.camel_plural} = await service.list();
    res.json({{ data: {n.camel_plural} }});
  }} catch (err) {{
    next(err); // handled by the centralized error middleware, BE084
  }}
}}

export async function create{n.pascal}(req: Request, res: Response, next: NextFunction) {{
  try {{
    // const parsed = {n.pascal}Schema.parse(req.body); // BE080
    const created = await service.create(req.body);
    res.status(201).json({{ data: created }});
  }} catch (err) {{
    next(err);
  }}
}}

export async function get{n.pascal}(req: Request, res: Response, next: NextFunction) {{
  try {{
    const {n.camel} = await service.getById(req.params.id);
    if (!{n.camel}) {{
      return res.status(404).json({{ error: {{ code: "not_found", message: "{n.pascal} not found" }} }});
    }}
    res.json({{ data: {n.camel} }});
  }} catch (err) {{
    next(err);
  }}
}}

export async function update{n.pascal}(req: Request, res: Response, next: NextFunction) {{
  try {{
    const updated = await service.update(req.params.id, req.body);
    res.json({{ data: updated }});
  }} catch (err) {{
    next(err);
  }}
}}

export async function delete{n.pascal}(req: Request, res: Response, next: NextFunction) {{
  try {{
    await service.remove(req.params.id);
    res.status(204).end();
  }} catch (err) {{
    next(err);
  }}
}}
"""
    service = f"""// Business logic, kept framework-agnostic (see references/backend-architecture.md).
// Replace these with real repository calls.

export async function list() {{
  return [];
}}
export async function create(input: unknown) {{
  return input;
}}
export async function getById(id: string) {{
  return null;
}}
export async function update(id: string, input: unknown) {{
  return input;
}}
export async function remove(id: string) {{
  return;
}}
"""
    return [
        (f"src/routes/{n.kebab}.routes.ts", routes),
        (f"src/controllers/{n.kebab}.controller.ts", controller),
        (f"src/services/{n.kebab}.service.ts", service),
    ]


def tpl_nestjs(n: Names):
    module = f"""import {{ Module }} from "@nestjs/common";
import {{ {n.pascal}Controller }} from "./{n.kebab}.controller";
import {{ {n.pascal}Service }} from "./{n.kebab}.service";

@Module({{
  controllers: [{n.pascal}Controller],
  providers: [{n.pascal}Service],
  exports: [{n.pascal}Service],
}})
export class {n.pascal}Module {{}}
"""
    controller = f"""import {{ Body, Controller, Delete, Get, Param, Patch, Post }} from "@nestjs/common";
import {{ {n.pascal}Service }} from "./{n.kebab}.service";
import {{ Create{n.pascal}Dto }} from "./dto/create-{n.kebab}.dto";

@Controller("{n.kebab_plural}")
export class {n.pascal}Controller {{
  constructor(private readonly service: {n.pascal}Service) {{}}

  @Get()
  list() {{
    return this.service.list();
  }}

  @Post()
  create(@Body() dto: Create{n.pascal}Dto) {{
    return this.service.create(dto);
  }}

  @Get(":id")
  get(@Param("id") id: string) {{
    return this.service.getById(id);
  }}

  @Patch(":id")
  update(@Param("id") id: string, @Body() dto: Partial<Create{n.pascal}Dto>) {{
    return this.service.update(id, dto);
  }}

  @Delete(":id")
  remove(@Param("id") id: string) {{
    return this.service.remove(id);
  }}
}}
"""
    service = f"""import {{ Injectable, NotFoundException }} from "@nestjs/common";

@Injectable()
export class {n.pascal}Service {{
  // Replace with real repository calls (see references/backend-architecture.md).

  async list() {{
    return [];
  }}
  async create(input: unknown) {{
    return input;
  }}
  async getById(id: string) {{
    return null;
  }}
  async update(id: string, input: unknown) {{
    return input;
  }}
  async remove(id: string) {{
    return;
  }}
}}
"""
    dto = f"""// Validation boundary for {n.pascal} creation (BE080).
// Add class-validator decorators once the real shape is known, e.g.:
//   @IsString() name: string;
export class Create{n.pascal}Dto {{}}
"""
    return [
        (f"src/{n.kebab}/{n.kebab}.module.ts", module),
        (f"src/{n.kebab}/{n.kebab}.controller.ts", controller),
        (f"src/{n.kebab}/{n.kebab}.service.ts", service),
        (f"src/{n.kebab}/dto/create-{n.kebab}.dto.ts", dto),
    ]


def tpl_fastapi(n: Names):
    schemas = f"""from pydantic import BaseModel


class {n.pascal}Create(BaseModel):
    \"\"\"Request body for creating a {n.snake}. Fill in real fields -- this is the
    validation boundary (BE080).\"\"\"
    pass


class {n.pascal}Out(BaseModel):
    id: str
"""
    router = f"""from fastapi import APIRouter, HTTPException

from ..schemas.{n.snake} import {n.pascal}Create, {n.pascal}Out

router = APIRouter(prefix="/{n.kebab_plural}", tags=["{n.kebab_plural}"])


@router.get("/")
async def list_{n.snake_plural}():
    return {{"data": []}}


@router.post("/", status_code=201)
async def create_{n.snake}(payload: {n.pascal}Create):
    # TODO: persist -- payload is already validated by Pydantic (BE080)
    return {{"data": payload}}


@router.get("/{{item_id}}")
async def get_{n.snake}(item_id: str):
    item = None  # TODO: fetch from persistence
    if item is None:
        raise HTTPException(status_code=404, detail="{n.pascal} not found")
    return {{"data": item}}


@router.patch("/{{item_id}}")
async def update_{n.snake}(item_id: str, payload: dict):
    return {{"data": payload}}


@router.delete("/{{item_id}}", status_code=204)
async def delete_{n.snake}(item_id: str):
    return None
"""
    return [
        (f"app/schemas/{n.snake}.py", schemas),
        (f"app/routers/{n.snake}.py", router),
    ]


def tpl_django(n: Names):
    serializers = f"""from rest_framework import serializers

# Replace with a real ModelSerializer once the {n.pascal} model exists.
# This is the validation boundary for this resource (BE080).


class {n.pascal}Serializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
"""
    views = f"""from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import {n.pascal}Serializer


class {n.pascal}ViewSet(viewsets.ViewSet):
    \"\"\"Replace with a ModelViewSet backed by a real queryset once the
    {n.pascal} model exists. Kept as a plain ViewSet so this file is valid
    before that model is written.\"\"\"

    def list(self, request):
        return Response({{"data": []}})

    def create(self, request):
        serializer = {n.pascal}Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({{"data": serializer.validated_data}}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        return Response({{"error": {{"code": "not_found", "message": "{n.pascal} not found"}}}}, status=404)

    def partial_update(self, request, pk=None):
        return Response({{"data": request.data}})

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
    urls = f"""from rest_framework.routers import DefaultRouter

from .views import {n.pascal}ViewSet

router = DefaultRouter()
router.register(r"{n.kebab_plural}", {n.pascal}ViewSet, basename="{n.kebab}")

urlpatterns = router.urls
"""
    return [
        (f"{n.snake}/serializers.py", serializers),
        (f"{n.snake}/views.py", views),
        (f"{n.snake}/urls.py", urls),
    ]


def tpl_supabase_edge(n: Names):
    fn = f"""// Supabase Edge Function for {n.kebab_plural} (Deno runtime).
// Deploy with: supabase functions deploy {n.kebab_plural}
// Most CRUD should go through the auto-generated REST/GraphQL API + RLS
// policies instead -- reach for an Edge Function only when logic can't be
// expressed as a Postgres function or RLS policy (see backend-architecture.md).

import {{ createClient }} from "npm:@supabase/supabase-js@2";

Deno.serve(async (req: Request) => {{
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  );

  try {{
    if (req.method === "GET") {{
      const {{ data, error }} = await supabase.from("{n.kebab_plural}").select("*");
      if (error) throw error;
      return Response.json({{ data }});
    }}

    if (req.method === "POST") {{
      const body = await req.json();
      // TODO: validate `body` at the boundary before inserting (BE080)
      const {{ data, error }} = await supabase.from("{n.kebab_plural}").insert(body).select().single();
      if (error) throw error;
      return Response.json({{ data }}, {{ status: 201 }});
    }}

    return Response.json(
      {{ error: {{ code: "method_not_allowed", message: `${{req.method}} not supported` }} }},
      {{ status: 405 }}
    );
  }} catch (err) {{
    console.error(err);
    return Response.json(
      {{ error: {{ code: "internal_error", message: "Something went wrong" }} }},
      {{ status: 500 }}
    );
  }}
}});
"""
    return [(f"supabase/functions/{n.kebab_plural}/index.ts", fn)]


TEMPLATES = {
    "nextjs-api": tpl_nextjs_api,
    "express": tpl_express,
    "nestjs": tpl_nestjs,
    "fastapi": tpl_fastapi,
    "django": tpl_django,
    "supabase-edge": tpl_supabase_edge,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("resource", help="Resource name, any case (e.g. 'order-item', 'OrderItem', 'order_item')")
    parser.add_argument("--stack", required=True, choices=STACKS)
    parser.add_argument("--output", type=Path, default=Path("./generated"), help="Project root to write into")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be written, don't write it")
    args = parser.parse_args()

    try:
        names = Names(args.resource)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    files = TEMPLATES[args.stack](names)

    for rel_path, content in files:
        target = args.output / rel_path
        if args.dry_run:
            print(f"--- would write {target} ---")
            print(content)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                print(f"skip (already exists): {target}", file=sys.stderr)
                continue
            target.write_text(content, encoding="utf-8")
            print(f"wrote {target}")

    if not args.dry_run:
        print(f"\n{len(files)} file(s) generated for '{args.resource}' ({args.stack}).")
        print("Fill in real validation, persistence, and auth before shipping -- see")
        print("references/backend-architecture.md and references/api-design.md.")


if __name__ == "__main__":
    main()
