import ParkingLotsPage from "./pages/ParkingLotsPage";
import ParkingGridPage from "./pages/ParkingGridPage";

function App() {
  return (
    // Mobile container
    <div class="max-w-sm bg-white mx-auto h-screen">
      <ParkingLotsPage />
      <ParkingGridPage />
    </div>
  );
}

export default App;
