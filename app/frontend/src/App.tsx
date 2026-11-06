import { CueSheet } from "./site/cue-sheet"
import { Header } from "./site/header"
import { Hero } from "./site/hero"
import { Closing, Footer, FourHands, History, LightTable, Research, Storyboard } from "./site/sections"
import { SketchFilters } from "./site/sketch"

export default function App() {
  return (
    <>
      <SketchFilters />
      <a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[60] focus:rounded-full focus:bg-pink focus:px-4 focus:py-2 focus:text-[#160a10]">Skip to content</a>
      <Header />
      <main id="main">
        <Hero />
        <CueSheet />
        <LightTable />
        <div id="hands"><FourHands /></div>
        <Storyboard />
        <History />
        <div id="research"><Research /></div>
        <Closing />
      </main>
      <Footer />
    </>
  )
}
