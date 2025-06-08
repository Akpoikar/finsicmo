import React from 'react';
import { useSimulationStore } from '../store/simulationStore';

interface InputFieldProps {
  label: string;
  field: 'ebitda' | 'interestRate' | 'multiple' | 'factorScore' | 'companyName' | 'description';
  type?: 'text' | 'number' | 'textarea';
  placeholder?: string;
  unit?: string;
}

export const InputField: React.FC<InputFieldProps> = ({
  label,
  field,
  type = 'text',
  placeholder = '',
  unit = '',
}) => {
  const store = useSimulationStore();
  const { currentTeam, updateField, toggleFieldStatus } = store;
  const data = store[field];

  const isReadOnly = currentTeam === 'team2';
  const isTextArea = type === 'textarea';

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const newValue = type === 'number' ? parseFloat(e.target.value) : e.target.value;
    updateField(field, newValue);
  };

  const handleStatusToggle = () => {
    if (currentTeam !== 'team1') {
      toggleFieldStatus(field);
    }
  };

  const getInputStyles = () => ({
    width: '100%',
    padding: 8,
    borderRadius: 6,
    border: '1px solid #cbd5e1',
    backgroundColor: isReadOnly ? '#f1f5f9' : 'white',
    color: isReadOnly ? '#6b7280' : '#111827',
    resize: 'none' as const,
  });

  return (
    <div style={{
      backgroundColor: 'white',
      border: '1px solid #e5e7eb',
      borderRadius: 8,
      padding: 16,
      marginBottom: 12,
      boxShadow: '0 1px 2px rgba(0,0,0,0.04)',
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
        <label style={{ fontSize: 14, fontWeight: 600 }}>{label}</label>
        <button
          onClick={handleStatusToggle}
          disabled={currentTeam === 'team1'}
          style={{
            padding: '4px 10px',
            fontSize: 12,
            borderRadius: 9999,
            border: '1px solid',
            cursor: currentTeam === 'team1' ? 'not-allowed' : 'pointer',
            backgroundColor: data.status === 'OK' ? '#d1fae5' : '#fef3c7',
            color: data.status === 'OK' ? '#065f46' : '#92400e',
            opacity: currentTeam === 'team1' ? 0.6 : 1,
          }}
        >
          {data.status}
        </button>
      </div>

      <div style={{ position: 'relative' }}>
        {isTextArea ? (
          <textarea
            value={data.value}
            onChange={handleChange}
            disabled={isReadOnly}
            placeholder={placeholder}
            rows={3}
            style={getInputStyles()}
          />
        ) : (
          <input
            type={type}
            value={data.value}
            onChange={handleChange}
            disabled={isReadOnly}
            placeholder={placeholder}
            style={getInputStyles()}
          />
        )}

        {unit && (
          <span style={{
            position: 'absolute',
            top: 8,
            right: 10,
            fontSize: 12,
            color: '#6b7280',
          }}>
            {unit}
          </span>
        )}
      </div>
    </div>
  );
};

export default InputField;
