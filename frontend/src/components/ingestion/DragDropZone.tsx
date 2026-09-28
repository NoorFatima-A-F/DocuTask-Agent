import React from 'react';
import { IngestionStudio } from '../../pages/IngestionStudio';

export interface DragDropZoneProps {
  onJobCreated?: (jobId: string, documentId: string) => void;
  onNavigateToReview?: (documentId: string) => void;
}

export const DragDropZone: React.FC<DragDropZoneProps> = (props) => {
  return <IngestionStudio {...props} />;
};
