import React from 'react';

interface EditorialSectionProps {
  sectionNumber: string;
  title: string;
  lede: string;
  annotation: string;
  method: string;
  children: React.ReactNode;
  secondary?: React.ReactNode;
}

export function EditorialSection({
  sectionNumber,
  title,
  lede,
  annotation,
  method,
  children,
  secondary,
}: EditorialSectionProps) {
  return (
    <section className="section-shell">
      <div className="section-head">
        <p className="section-kicker">{sectionNumber}</p>
        <h2 className="section-title">{title}</h2>
        <p className="section-lede">{lede}</p>
      </div>

      <div className="section-main">{children}</div>

      <aside className="section-aside">
        <p className="section-annotation">{annotation}</p>
        {secondary ? <div className="section-secondary">{secondary}</div> : null}
        <p className="section-method">{method}</p>
      </aside>
    </section>
  );
}
