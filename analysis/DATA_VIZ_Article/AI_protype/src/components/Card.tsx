import React from 'react';
interface CardProps {
  children: React.ReactNode;
  className?: string;
}
export function Card({ children, className = '' }: CardProps) {
  return (
    <div
      className={`bg-card border border-border rounded-card p-6 ${className}`}>

      {children}
    </div>);

}