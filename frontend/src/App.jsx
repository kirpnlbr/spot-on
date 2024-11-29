import { useState, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import ParkingLotsPage from "./pages/ParkingLotsPage";
import ParkingGridPage from "./pages/ParkingGridPage";
import NavigationPage from "./pages/NavigationPage";
import LocationPage from "./pages/LocationPage";
import BottomNav from './components/shared/BottomNav';
import PageTransition from './components/animations/PageTransition';

function App() {
  const [currentPage, setCurrentPage] = useState('location');
  const [selectedLot, setSelectedLot] = useState(null);
  const [locationEnabled, setLocationEnabled] = useState(false);
  const [selectedSpot, setSelectedSpot] = useState(null);
  const [direction, setDirection] = useState(1);

  const changePage = (newPage, transitionDirection) => {
    setDirection(transitionDirection);
    setCurrentPage(newPage);
  };

  const handleEnableLocation = () => {
    setLocationEnabled(true);
    changePage('lots', 1);
  };

  const handleSkipLocation = () => {
    changePage('lots', 1);
  };

  const handleSelectLot = (lot) => {
    setSelectedLot(lot);
    changePage('grid', 1);
  };

  const handleBackToLots = () => {
    changePage('lots', -1);
  };

  const handleSelectSpot = () => {
    changePage('navigation', 1);
  };

  const handleNavigate = () => {
    setSelectedSpot('A4');
    changePage('navigation', 1);
  };

  const handleBackToGrid = () => {
    changePage('grid', -1);
  };

  return (
    <div className="max-w-sm font-lexend bg-[#F2EFE9] mx-auto h-screen pb-16 relative overflow-hidden">
      <AnimatePresence mode="wait" initial={false}>
        {currentPage === 'location' && (
          <PageTransition key="location" direction={direction}>
            <LocationPage
              onEnableLocation={handleEnableLocation}
              onSkip={handleSkipLocation}
            />
          </PageTransition>
        )}

        {currentPage === 'lots' && (
          <PageTransition key="lots" direction={direction}>
            <ParkingLotsPage
              onSelectLot={handleSelectLot}
            />
          </PageTransition>
        )}

        {currentPage === 'grid' && (
          <PageTransition key="grid" direction={direction}>
            <ParkingGridPage
              lot={selectedLot}
              onBack={handleBackToLots}
              onSelectSpot={handleSelectSpot}
              onNavigate={handleNavigate}
            />
          </PageTransition>
        )}

        {currentPage === 'navigation' && (
          <PageTransition key="navigation" direction={direction}>
            <NavigationPage
              selectedLot={selectedLot}
              selectedSpot={selectedSpot}
              onBack={handleBackToGrid}
            />
          </PageTransition>
        )}
      </AnimatePresence>

      <BottomNav />
    </div>
  );
}

export default App;