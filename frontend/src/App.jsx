import ParkingLotsPage from "./pages/ParkingLotsPage";
import ParkingGridPage from "./pages/ParkingGridPage";
import NavigationPage from "./pages/NavigationPage";
import LocationPage from "./pages/LocationPage";

function App() {
  return (
    // Mobile container
    <div class="max-w-sm bg-[#fdfdfb] mx-auto h-screen">
      <LocationPage />
      <ParkingLotsPage />
      <ParkingGridPage />
      <NavigationPage />
    </div>
  );
}

export default App;
