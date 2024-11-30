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
  const [direction, setDirection] = useState(1);

  // Added navigationData state to hold the necessary data for navigation
  const [navigationData, setNavigationData] = useState({});

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

  const handleNavigate = (nearestSpotId, entryPoint, lotName, selectedLevel) => {
    // Set navigation data with the parameters received
    setNavigationData({ nearestSpotId, entryPoint, lotName, selectedLevel });
    changePage('navigation', 1);
  };

  const handleBackToGrid = () => {
    changePage('grid', -1);
  };

  return (
    <div class="max-w-sm font-geist bg-white mx-auto h-screen pb-16 relative overflow-hidden">
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
              onNavigate={handleNavigate}
            />
          </PageTransition>
        )}

        {currentPage === 'navigation' && (
          <PageTransition key="navigation" direction={direction}>
            <NavigationPage
              onBack={handleBackToGrid}
              // Passed the navigationData to NavigationPage
              nearestSpotId={navigationData.nearestSpotId}
              entryPoint={navigationData.entryPoint}
              lotName={navigationData.lotName}
              selectedLevel={navigationData.selectedLevel}
            />
          </PageTransition>
        )}
      </AnimatePresence>

      <BottomNav />
    </div>
  );
}

export default App;
