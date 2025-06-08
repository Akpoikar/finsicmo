import React from 'react';
import { Modal } from './Modal';
import { useSimulationStore } from '../store/simulationStore';

export const VideoModal: React.FC = () => {
  const { videoModalOpen, setVideoModalOpen } = useSimulationStore();

  return (
    <Modal
      isOpen={videoModalOpen}
      onClose={() => setVideoModalOpen(false)}
      title="Training Video"
    >
      <div className="aspect-video bg-gray-100 rounded-lg flex items-center justify-center">
        <div className="text-center">
          <div className="bg-blue-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
            <svg className="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 2L3 7v11h4v-6h6v6h4V7l-7-5z"/>
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Training Video</h3>
          <p className="text-gray-600 mb-4">
            This would contain an embedded training video explaining the valuation process and simulator usage.
          </p>
          <div className="bg-gray-200 rounded-lg p-8 text-gray-500">
            Video Player Placeholder
            <br />
            <span className="text-sm">Duration: 15:30</span>
          </div>
        </div>
      </div>
    </Modal>
  );
};