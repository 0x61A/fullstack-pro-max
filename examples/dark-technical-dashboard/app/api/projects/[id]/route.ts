import { NextRequest, NextResponse } from "next/server";

// GET /api/projects/[id]
export async function GET(request: NextRequest, { params }: { params: { id: string } }) {
  const projects = await findProjectsById(params.id);
  if (!projects) {
    return NextResponse.json(
      { error: { code: "not_found", message: "Projects not found" } },
      { status: 404 }
    );
  }
  return NextResponse.json({ data: projects });
}

// PATCH /api/projects/[id]
export async function PATCH(request: NextRequest, { params }: { params: { id: string } }) {
  const body = await request.json();
  // TODO: validate `body` at the boundary (BE080) before applying it
  const updated = await updateProjects(params.id, body);
  return NextResponse.json({ data: updated });
}

// DELETE /api/projects/[id]
export async function DELETE(request: NextRequest, { params }: { params: { id: string } }) {
  await deleteProjects(params.id);
  return new NextResponse(null, { status: 204 });
}

async function findProjectsById(id: string) {
  return null;
}
async function updateProjects(id: string, input: unknown) {
  return input;
}
async function deleteProjects(id: string) {
  return;
}
