import React from 'react';
interface PillProps {
  label: string;
  color: string;
  className?: string;
}
export function Pill({ label, color, className = '' }: PillProps) {
  return (
    <span
      className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${className}`}
      style={{
        backgroundColor: `${color}1A`,
        color: color
      }}>

      {label}
    </span>);

}