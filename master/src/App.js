import Home from "./pages/home/Home";
import Login from "./pages/login/Login";
import List from "./pages/list/List";
import Single from "./pages/single/Single";
import New from "./pages/new/New";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./style/dark.scss";
import { useContext } from "react";
import { DarkModeContext } from "./context/darkModeContext";
import React from "react";
import Register from "./pages/register/Register";


function App() {

  const { darkMode } = useContext(DarkModeContext);

  return (

     <div className={darkMode ? "app dark" : "app"}>
      <BrowserRouter>
        <Routes>
          <Route path="/">
            <Route index element={<Home />} />
            <Route path="login" element={<Login />} />
            <Route path="survey" element={<New />} />
            <Route path="chatbot" element={<List />} />
            <Route path="project" element={<Single />} />
            <Route path="register" element={<Register/>} />

              {/* <Route index element={<List />} /> */}
              {/* <Route path="new" element={<New/>}/> */}
              {/* </Route> */}
          </Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
