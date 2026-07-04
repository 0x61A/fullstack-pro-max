import { NextRequest, NextResponse } from "next/server";
// import { ProjectsSchema } from "@/lib/validation/projects";

// GET /api/projects -- list projects
export async function GET(request: NextRequest) {
  try {
    // TODO: read + validate query params (pagination, filters) -- see BE080
    const projects = await findProjectss();
    return NextResponse.json({ data: projects });
  } catch (err) {
    return errorResponse(err);
  }
}

// POST /api/projects -- create a new projects
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    // const parsed = ProjectsSchema.parse(body); // validate at the boundary, BE080
    const created = await createProjects(body);
    return NextResponse.json({ data: created }, { status: 201 });
  } catch (err) {
    return errorResponse(err);
  }
}

// Replace with real persistence -- these are placeholders so the route compiles.
async function findProjectss() {
  return [];
}
async function createProjects(input: unknown) {
  return input;
}

// Consistent error envelope, see references/api-design.md and BE082.
function errorResponse(err: unknown) {
  console.error(err);
  return NextResponse.json(
    { error: { code: "internal_error", message: "Something went wrong" } },
    { status: 500 }
  );
}
