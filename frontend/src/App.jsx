import ParkingLotsPage from "./pages/ParkingLotsPage";
import ParkingGridPage from "./pages/ParkingGridPage";
import NavigationPage from "./pages/NavigationPage";

function App() {
  return (
    // Mobile container
    <div class="max-w-sm bg-[#fdfdfb] mx-auto h-screen">
      <ParkingLotsPage />
      <ParkingGridPage />
      <NavigationPage />
    </div>
  );
}

export default App;
