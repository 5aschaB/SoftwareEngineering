import Home from "./pages/home/Home";
import Login from "./pages/login/Login";
import List from "./pages/list/List";
import Single from "./pages/single/Single";
import New from "./pages/new/New";
import { BrowserRouter, Routes, Route } from "react-router-dom";

// REACT ROUTER DOM NOT DONE AS INTEGRATION INTO FLASK INSTEAD 

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/">
            <Route index element={<Home />} />
            <Route path="login" element={<Login />} />
            <Route path="survey" element={<New />} />
            <Route path="users">
              <Route index element={<List />} />
              {/* <Route path="new" element={<New/>}/> */}
              </Route>

          </Route>
        </Routes>
      </BrowserRouter>


    </div>
  );
}

export default App;
