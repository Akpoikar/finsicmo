import React from 'react';
import {Modal} from './Modal'; // assuming default export
import { useSimulationStore } from '../store/simulationStore';

export const TextModal = () => {
  const { textModalOpen, setTextModalOpen } = useSimulationStore();

  const guideText = `
    Welcome to the valuation tool. This platform allows you to simulate different financial outcomes
    using multiple models — including DCF, comps, and transaction analysis. You can collaborate with others
    or work alone, depending on the team mode selected.

    Try adjusting the EBITDA, multiples, and discount rates to explore different scenarios.
    Visual outputs will update as you go.
  `;

  return (
    <Modal
      isOpen={textModalOpen}
      onClose={() => setTextModalOpen(false)}
      title="User Guide"
    >
      <div style={{ padding: '1.5rem', backgroundColor: '#f1f5ff', borderRadius: '8px', border: '1px solid #cbd5e1' }}>
        <h3 style={{ fontWeight: '600', fontSize: '1.2rem', marginBottom: '0.75rem' }}>
          How to Use the Simulator
        </h3>
        <p style={{ lineHeight: 1.6, color: '#334155', whiteSpace: 'pre-line' }}>
          {guideText}
        </p>
      </div>

      <div style={{ marginTop: 24, display: 'flex', gap: 16, flexWrap: 'wrap' }}>
        <div style={{ flex: 1, minWidth: 200, backgroundColor: '#e8fbe6', padding: 16, borderRadius: 8, border: '1px solid #a7f3d0' }}>
          <h4 style={{ marginBottom: 8, fontWeight: 500, color: '#065f46' }}>Team 1 Mode</h4>
          <p style={{ fontSize: 14, color: '#065f46' }}>
            Can input values and set core assumptions. Focused on entering data.
          </p>
        </div>
        <div style={{ flex: 1, minWidth: 200, backgroundColor: '#fff7ed', padding: 16, borderRadius: 8, border: '1px solid #fdba74' }}>
          <h4 style={{ marginBottom: 8, fontWeight: 500, color: '#9a3412' }}>Team 2 Mode</h4>
          <p style={{ fontSize: 14, color: '#9a3412' }}>
            Limited to review only — can accept/reject but not change inputs.
          </p>
        </div>
      </div>
    </Modal>
  );
};

export default TextModal;
