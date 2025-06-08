// Represents each input box's data
export interface InputFieldData {
  value: string | number;
  status: 'TBD' | 'OK'; // initial or confirmed
}

// Global app state shape
export interface SimulationState {
  // Fields the user can change
  ebitda: InputFieldData;
  interestRate: InputFieldData;
  multiple: InputFieldData;
  factorScore: InputFieldData;
  companyName: InputFieldData;
  description: InputFieldData;

  // User team - controls behavior
  currentTeam: 'team1' | 'team2';

  // Time tracking
  elapsedTime: number;
  currentStage: string;
  nextStage: string;
  nextStageDuration: string; // e.g., "1 hr"

  // UI Modals
  videoModalOpen: boolean;
  textModalOpen: boolean;

  // Derived values
  valuation: number;
  isAgreed: boolean;
}

// For stage tracking logic
export interface Stage {
  name: string;
  duration: number; // seconds
}

// Store actions, split into simpler pieces
export interface SimulationActions {
  updateField: (
    field: 'ebitda' | 'interestRate' | 'multiple' | 'factorScore' | 'companyName' | 'description',
    value: string | number
  ) => void;

  toggleFieldStatus: (
    field: 'ebitda' | 'interestRate' | 'multiple' | 'factorScore' | 'companyName' | 'description'
  ) => void;

  setTeam: (team: 'team1' | 'team2') => void;
  incrementTime: () => void;
  setVideoModalOpen: (open: boolean) => void;
  setTextModalOpen: (open: boolean) => void;
}
