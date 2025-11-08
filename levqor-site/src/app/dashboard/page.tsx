import { auth } from "@/auth";
import { redirect } from "next/navigation";
import DashboardTiles from "@/components/DashboardTiles";

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
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="bg-white rounded-lg shadow p-6 border-b border-gray-200">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">
            Welcome back, {session.user.email}
          </p>
        </div>
        
        {!usage || Object.keys(usage).length === 0 ? (
          <div className="space-y-6">
            <div className="text-center py-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Get Started with Levqor</h2>
              <p className="text-gray-600">You haven't created any workflows yet. Let's get started!</p>
            </div>
            <DashboardTiles />
          </div>
        ) : (
          <div className="bg-white border rounded-lg p-6 shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Usage Summary</h2>
            <pre className="text-sm bg-gray-50 p-4 rounded border overflow-auto">
              {JSON.stringify(usage, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </main>
  );
}
