import React from 'react';
import { useSimulationStore } from '../store/simulationStore';
import { Timer } from '../components/Timer';
import { InputField } from '../components/InputField';
import { PieChart } from '../components/PieChart';
import { Sidebar } from '../components/Sidebar';
import { VideoModal } from '../components/VideoModal';
import { TextModal } from '../components/TextModal';

export const SimulationPage: React.FC = () => {
  const { currentTeam, setTeam, valuation, isAgreed } = useSimulationStore();

  const handleSubmit = () => {
    // placeholder logic for now - maybe send to backend later?
    window.alert("Submission successful."); 
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Bar */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Team Mode Toggle */}
            <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
              <button
                onClick={() => setTeam('team1')}
                className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all duration-200 ${
                  currentTeam === 'team1'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Team 1
              </button>
              <button
                onClick={() => setTeam('team2')}
                className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all duration-200 ${
                  currentTeam === 'team2'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Team 2
              </button>
            </div>

            {/* Timer */}
            <Timer />
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Sidebar */}
          <div className="lg:col-span-2">
            <Sidebar />
          </div>

          {/* Center Section */}
          <div className="lg:col-span-6 space-y-6">
           
            {/* Valuation Inputs */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Valuation Inputs</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <InputField
                  label="EBITDA"
                  field="ebitda"
                  type="number"
                  placeholder="Enter EBITDA"
                  unit="$ million"
                />
                <InputField
                  label="Multiple"
                  field="multiple"
                  type="number"
                  placeholder="Enter multiple"
                  unit="x"
                />
                <InputField
                  label="Factor Score"
                  field="factorScore"
                  type="number"
                  placeholder="1-5 score"
                />
                <InputField
                label="Interest Rate"
                field="interestRate"
                type="number"
                placeholder="Enter rate"
                unit="%"
              />
              </div>
            </div>
                        
            {/* Company Information */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Company Information</h3>
              <InputField
                label="Company Name"
                field="companyName"
                type="text"
                placeholder="Enter company name"
              />
              <InputField
                label="Description"
                field="description"
                type="textarea"
                placeholder="Enter detailed description..."
              />
            </div>
            <button
              onClick={handleSubmit}
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200 shadow-sm hover:shadow-md"
            >
              Submit Analysis
            </button>
            
          </div>

          {/* Right Panel */}
          <div className="lg:col-span-4 space-y-6">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="text-center">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Current Valuation</h3>
                <div className="text-4xl font-bold text-blue-600">
                  ${valuation.toFixed(1)}M
                </div>
                <div className="mt-2">
                  {isAgreed ? (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                      <svg className="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      Agreed by Team 2
                    </span>
                  ) : (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-orange-100 text-orange-800">
                      <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Pending Team 2 Approval
                    </span>
                  )}
                </div>
              </div>
            </div>
            
            <PieChart />
          </div>
        </div>
      </div>

      {/* Modals */}
      <VideoModal />
      <TextModal />
    </div>
  );
};