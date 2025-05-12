'use client';

import React, { useEffect, useRef, useState } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { EventRenderer } from './EventRenderer';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

type EventMessage = {
  event_type: string;
  event_data: any;
};

export function ResearchClient({ clientId }: { clientId: string }) {
  const [events, setEvents] = useState<EventMessage[]>([]);
  const [input, setInput] = useState('');
  const [connected, setConnected] = useState(false);
  const [showProgress, setShowProgress] = useState(false);
  const [progress, setProgress] = useState(0); // To track loader progress
  const socketRef = useRef<WebSocket | null>(null);
  const dropdownRef = useRef<HTMLDivElement | null>(null);
  const [triggered, setTriggered] = useState(false);

  


  const progressStages = [
    "followup_result",
    "research_plan_generated",
    "plan_execution_steps",
    "learnings_extracted",
    "final_report_compilation",
    "report_generated_saved",
  ];
  

 

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/api/v1/generate_report?client_id=${clientId}`);
    socketRef.current = ws;

    ws.onopen = () => {
      setConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data: EventMessage = JSON.parse(event.data);

        if (data.event_type === 'followup_result') {
          setShowProgress(true);
          setProgress((prev) => prev + 20); // Example progress increment
        }
        if (data.event_type === 'report_generated_saved') {
          setShowProgress(false);
          setProgress(100); // Complete when report is generated
        }

        setEvents((prev) => [...prev, data]);
        if (data.event_type === 'followup_result') setTriggered(true);

      } catch {
        setEvents((prev) => [...prev, { event_type: 'message', event_data: event.data }]);
      }
    };

    ws.onclose = () => {
      setConnected(false);
    };

    return () => {
      ws.close();
    };
  }, [clientId]);

  const handleSend = () => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(input);
      setInput('');
    }
  };

  useEffect(() => {
    const receivedStages = new Set(
      events
        .map((e) => e.event_type)
        .filter((type) => progressStages.includes(type))
    );
    const progressPercentage = (receivedStages.size / progressStages.length) * 100;
    setProgress(progressPercentage);
  }, [events]);

  useEffect(() => {
    if (triggered && progress < 100) {
      setShowProgress(true);
    } else if (progress === 100) {
      const timeout = setTimeout(() => {
        setShowProgress(false);
      }, 2000);
      return () => clearTimeout(timeout);
    }
  }, [progress, triggered]);
  
  
  

  const finalReport = events.find((e) => e.event_type === 'report_generated_saved');
  const intermediateEvents = events.filter((e) => e.event_type !== 'report_generated_saved');

  useEffect(() => {
    if (dropdownRef.current) {
      dropdownRef.current.scrollTo({
        top: dropdownRef.current.scrollHeight,
        behavior: 'smooth',
      });
    }
  }, [events]);

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6 relative">
      {/* Progress Bar */}
      {showProgress && (
  <div className="absolute top-16 w-full transition-all duration-300">
    <div className="h-1 bg-gray-200 rounded-full overflow-hidden">
      <div
        className={`h-full transition-all duration-500 ${
          progress === 100 ? 'bg-green-500' : 'bg-blue-500'
        }`}
        style={{ width: `${progress}%` }}
      />
    </div>
    <p className="text-xs text-muted-foreground mt-1">
      {progress === 100 ? '✅ Report Generated!' : '⚙️ Executing research...'}
    </p>
  </div>
)}

      {/* Execution Stream Dropdown */}
      <div>
        <Accordion type="single" collapsible defaultValue="agent-details">
          <AccordionItem value="agent-details">
            <AccordionTrigger className="text-md font-medium">Execution Stream</AccordionTrigger>
            <AccordionContent>
  <div
    ref={dropdownRef}
    className="h-64 overflow-y-scroll scrollbar-hide pr-2"
  >
    <div className="space-y-4 mt-2">
      {intermediateEvents.map((event, idx) => (
        <Card key={idx} className="bg-muted shadow">
          <CardContent className="p-4">
            <EventRenderer event={event} />
          </CardContent>
        </Card>
      ))}
    </div>
  </div>
</AccordionContent>
          </AccordionItem>
        </Accordion>
      </div>
  
      {/* Final Report (moved down to avoid overlap) */}
      {finalReport && (
        <div className="space-y-2 mt-6 mb-20">
          <h2 className="text-xl font-bold">📄 Final Report</h2>
          <Card className="bg-background shadow">
            <CardContent className="p-4">
              <EventRenderer event={finalReport} />
            </CardContent>
          </Card>
        </div>
      )}
  
      {/* Input at bottom */}
      <div className="fixed bottom-4 left-0 right-0 mx-auto w-full max-w-4xl p-4 box-border flex items-center gap-2 bg-background z-10">
        <Input
          placeholder="Ask your research question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={!connected}
          className="flex-grow"
        />
        <Button onClick={handleSend} disabled={!connected || input === ''}>
          Send
        </Button>
      </div>
    </div>
  );
}
