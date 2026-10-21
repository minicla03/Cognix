import { LegalDocumentLayout } from "@/components/legal-document-layout";
const sections = [
  "Introduction",
  "Account",
  "Acceptable Use",
  "User Content",
  "AI-Generated Content",
  "Intellectual Property",
  "Service Availability",
  "Third-Party Services",
  "Account Termination",
  "Disclaimers",
  "Limitation of Liability",
  "Changes to the Service",
  "Contact",
].map((title) => ({ title }));
export default function TermsPage() {
  return (
    <LegalDocumentLayout
      title="Terms of Service"
      intro="This page provides the structure for Cognix’s terms. The final terms will be added after legal review."
      sections={sections}
    />
  );
}
