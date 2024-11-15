import { useState } from 'react';
import ParkingLotsPage from "./pages/ParkingLotsPage";
import ParkingGridPage from "./pages/ParkingGridPage";
import NavigationPage from "./pages/NavigationPage";
import LocationPage from "./pages/LocationPage";

function App() {
  const [currentPage, setCurrentPage] = useState('location');
  const [selectedLot, setSelectedLot] = useState(null);
  const [locationEnabled, setLocationEnabled] = useState(false);

  return (
    <div className="max-w-sm font-lexend bg-[#fdfdfb] mx-auto h-screen">
      {/* Location Page */}
      {currentPage === 'location' && (
        <LocationPage
          onEnableLocation={() => {
            setLocationEnabled(true);
            setCurrentPage('lots');
          }}
          onSkip={() => {
            setCurrentPage('lots');
          }}
        />
      )}

      {/* Parking Lots Page */}
      {currentPage === 'lots' && (
        <ParkingLotsPage
          onSelectLot={(lot) => {
            setSelectedLot(lot);
            setCurrentPage('grid');
          }}
        />
      )}

      {/* Parking Grid Page */}
      {currentPage === 'grid' && (
        <ParkingGridPage
          lot={selectedLot}
          onBack={() => setCurrentPage('lots')}
          onSelectSpot={() => setCurrentPage('navigation')}
        />
      )}

      {/* Navigation Page */}
      {currentPage === 'navigation' && (
        <NavigationPage
          onBack={() => setCurrentPage('grid')}
        />
      )}
    </div>
  );
}

export default App;
