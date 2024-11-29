import { useState, useEffect } from 'react';
import ParkingLotsPage from "./pages/ParkingLotsPage";
import ParkingGridPage from "./pages/ParkingGridPage";
import NavigationPage from "./pages/NavigationPage";
import LocationPage from "./pages/LocationPage";

function App() {
  const [currentPage, setCurrentPage] = useState('location');
  const [selectedLot, setSelectedLot] = useState(null);
  const [locationEnabled, setLocationEnabled] = useState(false);
  const [selectedSpot, setSelectedSpot] = useState(null);

  const handleEnableLocation = () => {
    setLocationEnabled(true);
    setCurrentPage('lots');
  };

  const handleSkipLocation = () => {
    setCurrentPage('lots');
  };

  const handleSelectLot = (lot) => {
    setSelectedLot(lot);
    setCurrentPage('grid');
  };

  const handleBackToLots = () => {
    setCurrentPage('lots');
  };

  const handleSelectSpot = () => {
    setCurrentPage('navigation');
  };

  const handleNavigate = () => {
    setSelectedSpot('A4');
    setCurrentPage('navigation');
  };

  const handleBackToGrid = () => {
    setCurrentPage('grid');
  };

  return (
    <div class="max-w-sm font-lexend bg-[#F2EFE9] mx-auto h-screen">
      {/* Location Page */}
      {currentPage === 'location' && (
        <LocationPage
          onEnableLocation={handleEnableLocation}
          onSkip={handleSkipLocation}
        />
      )}

      {/* Parking Lots Page */}
      {currentPage === 'lots' && (
        <ParkingLotsPage
          onSelectLot={handleSelectLot}
        />
      )}

      {/* Parking Grid Page */}
      {currentPage === 'grid' && (
        <ParkingGridPage
          lot={selectedLot}
          onBack={handleBackToLots}
          onSelectSpot={handleSelectSpot}
          onNavigate={handleNavigate}
        />
      )}

      {/* Navigation Page */}
      {currentPage === 'navigation' && (
        <NavigationPage
          selectedLot={selectedLot}
          selectedSpot={selectedSpot}
          onBack={handleBackToGrid}
        />
      )}
    </div>
  );
}


export default App;
