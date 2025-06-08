import React, { useEffect } from 'react';
import { Clock } from 'lucide-react';
import { useSimulationStore } from '../store/simulationStore';

export const Timer = () => {
  const {
    elapsedTime,
    currentStage,
    nextStage,
    nextStageDuration,
    incrementTime,
  } = useSimulationStore();

  useEffect(() => {
    const tick = setInterval(() => {
      incrementTime();
    }, 1000);

    return () => {
      clearInterval(tick);
    };
  }, []);

  const formatTime = (s: number) => {
    const h = Math.floor(s / 3600);
    const m = Math.floor((s % 3600) / 60);
    const sec = s % 60;

    return [
      h.toString().padStart(2, '0'),
      m.toString().padStart(2, '0'),
      sec.toString().padStart(2, '0'),
    ].join(':');
  };

  return (
    <div
      className="flex items-center space-x-3 px-4 py-2 border rounded"
      style={{ backgroundColor: '#f9fafb' }}
    >
      <div style={{ background: '#dbeafe', padding: 6, borderRadius: 6 }}>
        <Clock size={16} color="#2563eb" />
      </div>
      <div>
        <div className="text-sm font-mono font-bold">
          {formatTime(elapsedTime)}
        </div>
        <div style={{ fontSize: 12, color: '#4b5563' }}>
          {currentStage}
          {nextStage ? (
            <>
              <span style={{ margin: '0 6px' }}>→</span>
              {nextStage}
              {nextStageDuration ? (
                <span style={{ marginLeft: 4, color: '#9ca3af' }}>
                  ({nextStageDuration})
                </span>
              ) : null}
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default Timer;
