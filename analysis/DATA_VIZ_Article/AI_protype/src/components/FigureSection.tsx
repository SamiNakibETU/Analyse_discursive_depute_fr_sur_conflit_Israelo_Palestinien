import React from 'react';
interface FigureSectionProps {
  title: string;
  subtitle: string;
  source: string;
  children: React.ReactNode;
}
export function FigureSection({
  title,
  subtitle,
  source,
  children
}: FigureSectionProps) {
  return (
    <section className="flex flex-col w-full">
      <div className="mb-6">
        <h2 className="font-sans font-semibold text-[24px] tracking-tight text-text-primary">
          {title}
        </h2>
        <p className="font-sans font-normal text-[14px] text-text-secondary mt-1">
          {subtitle}
        </p>
      </div>

      <div className="w-full">{children}</div>

      <div className="mt-4">
        <p className="font-sans font-normal text-[11px] text-text-muted italic">
          {source}
        </p>
      </div>
    </section>);

}