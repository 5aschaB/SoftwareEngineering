import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { DarkModeContextProvider } from "./context/darkModeContext";
import { registerLicense } from '@syncfusion/ej2-base';

registerLicense('ORg4AjUWIQA/Gnt2VVhkQlFacldJXnxLeEx0RWFab1p6d1NMYFlBNQtUQF1hSn5RdEFjXXxYdHBVRWhc');

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <DarkModeContextProvider>
    <App />
    </DarkModeContextProvider>

  </React.StrictMode>
);

