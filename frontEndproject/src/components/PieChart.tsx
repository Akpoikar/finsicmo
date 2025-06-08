import React from 'react';
import { PieChart as RechartsPieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { useSimulationStore } from '../store/simulationStore';

export const PieChart: React.FC = () => {
  const { valuation, ebitda, multiple, factorScore, interestRate, isAgreed } = useSimulationStore();

  const ebitdaValue = Number(ebitda.value) || 0;
  const multipleValue = Number(multiple.value) || 0;
  const factorScoreValue = Number(factorScore.value) || 1;
  const interestRateValue = Number(interestRate.value) || 0;

  // Calculate base valuation (EBITDA × Multiple × Factor Score)
  const baseValuation = ebitdaValue * multipleValue * factorScoreValue;

  const data = [
    { 
      name: 'Base Valuation', 
      value: 100 - interestRateValue,
      details: `$${baseValuation.toFixed(1)}M`,
      percentage: 100 - interestRateValue,
      description: 'EBITDA × Multiple × Factor Score'
    },
    { 
      name: 'Interest Rate', 
      value: interestRateValue,
      details: `${interestRateValue}%`,
      percentage: interestRateValue,
      description: 'Reduces valuation by this percentage'
    }
  ];

  const COLORS = ['#3B82F6', '#EF4444'];

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
      <div className="space-y-8">
        {/* Chart */}
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <RechartsPieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                outerRadius={100}
                innerRadius={60}
                paddingAngle={2}
                dataKey="value"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                formatter={(value: number, name: string, entry: any) => [
                  entry.payload.details,
                  name
                ]}
                contentStyle={{
                  backgroundColor: 'white',
                  border: '1px solid #e5e7eb',
                  borderRadius: '0.5rem',
                  padding: '0.75rem'
                }}
              />
            </RechartsPieChart>
          </ResponsiveContainer>
        </div>

        {/* Legend */}
        <div className="space-y-4">
          {data.map((item, index) => (
            <div key={item.name} className="flex items-start space-x-3">
              <div 
                className="w-4 h-4 rounded-full mt-1 flex-shrink-0" 
                style={{ backgroundColor: COLORS[index] }}
              />
              <div className="flex-grow">
                <div className="flex items-center justify-between">
                  <span className="text-base font-medium text-gray-900">{item.name}</span>
                  <span className="text-base font-bold" style={{ color: COLORS[index] }}>
                    {item.details}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mt-0.5">{item.description}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Formula */}
        <div className="border-t border-gray-200 pt-4">
          <div className="text-base text-gray-900">
            <div className="font-medium mb-2">Valuation Formula</div>
            <div className="flex items-center justify-center space-x-3 text-lg">
              <span className="font-mono text-blue-600">${baseValuation.toFixed(1)}M</span>
              <span className="text-gray-400">×</span>
              <span className="font-mono text-red-600">{(1 - interestRateValue/100).toFixed(2)}</span>
              <span className="text-gray-400">=</span>
              <span className="font-mono font-bold">${valuation.toFixed(1)}M</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};