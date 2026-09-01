import Header from "./components/Header";
import Hero from "./components/Hero";
import HowItWorks from "./components/HowItWorks";
import AnalyzerPanel from "./components/AnalyzerPanel";
import MethodAndFooter from "./components/MethodAndFooter";

export default function App() {
  return (
    <div className="min-h-screen bg-paper">
      <Header />
      <Hero />
      <HowItWorks />
      <AnalyzerPanel />
      <MethodAndFooter />
    </div>
  );
}
