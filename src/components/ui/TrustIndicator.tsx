import React from 'react';
import { polishTokens } from '../../design-system/tokens/polish';

export type TrustStateType = keyof typeof polishTokens.trustStates;

export interface TrustIndicatorProps extends React.HTMLAttributes<HTMLSpanElement> {
  state: TrustStateType;
  customLabel?: string;
  showIcon?: boolean;
}

export const TrustIndicator: React.FC<TrustIndicatorProps> = ({
  state,
  customLabel,
  showIcon = true,
  className = '',
  ...props
}) => {
  const config = polishTokens.trustStates[state] || polishTokens.trustStates.UNKNOWN;

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-mono font-medium border transition-all ${className}`}
      style={{
        backgroundColor: config.bg,
        borderColor: config.border,
        color: config.color,
      }}
      title={`Trust Class: ${config.label}`}
      {...props}
    >
      {showIcon && <span className="text-[11px]">{config.icon}</span>}
      <span>{customLabel || config.label}</span>
    </span>
  );
};
