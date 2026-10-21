import { LegalDocumentLayout } from "@/components/legal-document-layout";
const sections = [
  "Data Controller",
  "Data We Collect",
  "How We Use Data",
  "User Content and Uploaded Documents",
  "AI Processing",
  "Data Storage",
  "Third-Party Services",
  "Data Retention",
  "Security",
  "International Data Transfers",
  "User Rights",
  "Account Deletion",
  "Cookies",
  "Changes to This Policy",
  "Contact",
].map((title) => ({ title }));
export default function PrivacyPage() {
  return (
    <LegalDocumentLayout
      title="Privacy Policy"
      intro="This page provides the structure for Cognix’s privacy information. The final policy content will be added after legal review."
      sections={sections}
    />
  );
}
