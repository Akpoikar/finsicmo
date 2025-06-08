import React from 'react';
import { Video, HelpCircle } from 'lucide-react';
import { useSimulationStore } from '../store/simulationStore';

export const Sidebar = () => {
  const { setVideoModalOpen, setTextModalOpen } = useSimulationStore();

  return (
    <div style={{
      background: 'white',
      border: '1px solid #e5e7eb',
      borderRadius: 8,
      padding: 16,
      boxShadow: '0 1px 2px rgba(0,0,0,0.05)'
    }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <button
          onClick={() => setVideoModalOpen(true)}
          title="Training Video"
          style={{
            backgroundColor: '#dbeafe',
            padding: '16px',
            borderRadius: 8,
            border: 'none',
            textAlign: 'center',
            transition: 'all 0.2s',
          }}
          onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#bfdbfe'}
          onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#dbeafe'}
        >
          <Video size={24} color="#2563eb" style={{ display: 'block', margin: '0 auto' }} />
          <div style={{ fontSize: 12, marginTop: 6, color: '#374151' }}>Training Video</div>
        </button>

        <button
          onClick={() => setTextModalOpen(true)}
          title="Help & Info"
          style={{
            backgroundColor: '#d1fae5',
            padding: '16px',
            borderRadius: 8,
            border: 'none',
            textAlign: 'center',
            transition: 'all 0.2s',
          }}
          onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#a7f3d0'}
          onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#d1fae5'}
        >
          <HelpCircle size={24} color="#059669" style={{ display: 'block', margin: '0 auto' }} />
          <div style={{ fontSize: 12, marginTop: 6, color: '#065f46' }}>Help & Info</div>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
