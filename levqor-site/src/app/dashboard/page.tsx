import { auth } from "@/auth";
import { redirect } from "next/navigation";

export const dynamic = "force-dynamic";

async function getUsage(){
  const api = process.env.NEXT_PUBLIC_API_URL!;
  try {
    const res = await fetch(`${api}/api/usage/summary`, { cache: "no-store" });
    if(!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

export default async function Dashboard(){
  const session = await auth();
  
  if(!session?.user){
    redirect('/signin');
  }
  
  const usage = await getUsage();
  
  return (
    <main className="p-8 max-w-4xl mx-auto space-y-6">
      <div className="border-b pb-4">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-gray-600 mt-1">
          Signed in as {session.user.email}
        </p>
      </div>
      
      <div className="bg-white border rounded-lg p-6 shadow-sm">
        <h2 className="text-xl font-semibold mb-4">Usage Summary</h2>
        <pre className="text-sm bg-gray-50 p-4 rounded border overflow-auto">
          {JSON.stringify(usage, null, 2) || "No usage data available"}
        </pre>
      </div>
      
      <div className="text-sm text-gray-500">
        <p>API: {process.env.NEXT_PUBLIC_API_URL}</p>
      </div>
    </main>
  );
}
