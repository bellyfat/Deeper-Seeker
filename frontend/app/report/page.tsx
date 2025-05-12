import { ResearchClient } from '@/app/components/ResearchClient';
import { v4 as uuidv4 } from 'uuid';

export default function Page() {
  // You can persist client_id in localStorage/session later
  const clientId = uuidv4();

  return (
    <main className="min-h-screen bg-background text-foreground p-6">
      <h1 className="text-2xl font-bold mb-4">AI Research Assistant</h1>
      <ResearchClient clientId={clientId} />
    </main>
  );
}
