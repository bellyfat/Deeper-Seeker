import React from 'react';
import ReactMarkdown from 'react-markdown';

export function EventRenderer({ event }: { event: { event_type: string; event_data: any } }) {
  const { event_type, event_data } = event;

  switch (event_type) {
    case "message":
      return <p>{event_data}</p>;

    case "followup_result": {
      const initial = event_data?.initial_query;
      const questions = event_data?.followup_questions ?? [];

      return (
        <div>
          <div className="font-semibold">🧠 Follow-up Questions Generated:</div>
          <p className="text-sm mb-2 italic">Initial: {initial}</p>
          <ul className="list-disc pl-5 text-sm">
            {questions.map((q: string, i: number) => (
              <li key={i}>{q}</li>
            ))}
          </ul>
        </div>
      );
    }

    case "research_plan_generated": {
      const stepsObject = event_data ?? {};
      const steps = Object.entries(stepsObject).map(([stepKey, description]) => `${stepKey}: ${description}`);

      return (
        <div>
          <div className="font-semibold">📋 Research Plan:</div>
          {steps.length === 0 ? (
            <p className="text-sm italic text-muted-foreground">No steps found</p>
          ) : (
            <ol className="list-decimal pl-6 mt-1 text-sm">
              {steps.map((step: string, i: number) => (
                <li key={i}>{step}</li>
              ))}
            </ol>
          )}
        </div>
      );
    }

    case "plan_execution_steps": {
      const step = event_data?.plan_step;
      const queries = event_data?.search_queries ?? [];

      return (
        <div className="border p-4 rounded bg-muted">
          <div className="font-semibold mb-1">🧩 Plan Step Execution:</div>
          <p className="text-sm mb-2">{step}</p>
          <div className="text-xs text-muted-foreground">Search Queries:</div>
          <ul className="list-disc pl-5 text-sm mt-1">
            {queries.map((q: string, i: number) => (
              <li key={i}>{q}</li>
            ))}
          </ul>
          <div className="mt-2 text-xs text-blue-500 italic">Status: In Progress</div>
        </div>
      );
    }

    case "learnings_extracted":
      return (
        <div>
          <div className="font-semibold">📘 Key Learnings:</div>
          <p className="text-sm whitespace-pre-wrap">Learnings and content extracted</p>
        </div>
      );

    case "final_report_compilation":
      return (
        <div className="text-sm text-muted-foreground italic">
          📝 Compiling final report...
        </div>
      );

    case "report_generated_saved":
      return (
        <div>
          <div className="font-semibold">✅ Final Report:</div>
          {/* Render the event_data (Markdown content) using ReactMarkdown */}
          <div className="mt-2">
            <ReactMarkdown
              children={event_data}
              components={{
                h1({node, ...props}) {
                  return <h1 className="text-2xl font-bold my-4" {...props} />;
                },
                h2({node, ...props}) {
                  return <h2 className="text-xl font-semibold my-3" {...props} />;
                },
                h3({node, ...props}) {
                  return <h3 className="text-lg font-medium my-2" {...props} />;
                },
                p({node, ...props}) {
                  return <p className="text-sm my-2" {...props} />;
                },
                a({node, ...props}) {
                  return <a className="text-blue-600" {...props} />;
                },
                ul({node, ...props}) {
                  return <ul className="list-disc pl-5 text-sm my-2" {...props} />;
                },
                ol({node, ...props}) {
                  return <ol className="list-decimal pl-6 text-sm my-2" {...props} />;
                },
                li({node, ...props}) {
                  return <li className="text-sm my-1" {...props} />;
                },
                strong({node, ...props}) {
                  return <strong className="font-semibold" {...props} />;
                },
                em({node, ...props}) {
                  return <em className="italic" {...props} />;
                },
                blockquote({node, ...props}) {
                  return <blockquote className="border-l-4 pl-4 italic my-4" {...props} />;
                }
              }}
            />
          </div>
        </div>
      );

    default:
      return (
        <div className="text-sm text-muted-foreground">
          ⚠️ Unknown event type: <span className="font-mono">{event_type}</span>
        </div>
      );
  }
}
