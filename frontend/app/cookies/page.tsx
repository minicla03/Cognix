import { LegalDocumentLayout } from "@/components/legal-document-layout";
const sections = [
  "Necessary cookies",
  "Preference cookies",
  "Analytics cookies",
  "Marketing cookies",
  "Managing preferences",
].map((title) => ({
  title,
  body:
    title === "Managing preferences"
      ? "Cookie configuration will be finalized before production deployment."
      : "[Information about this category will be provided after product and legal review.]",
}));
export default function CookiesPage() {
  return (
    <LegalDocumentLayout
      title="Cookies"
      intro="This page explains the cookie categories Cognix may support. It does not claim that any optional category is currently active."
      sections={sections}
    />
  );
}
