import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import PrivateRoute from './components/PrivateRoute';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import TemplateList from './pages/TemplateList';
import AdminTemplateList from './pages/admin/AdminTemplateList';
import AdminTemplateCreate from './pages/admin/AdminTemplateCreate';
import PaymentPage from './pages/PaymentPage';

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/payment" element={<PaymentPage />} />
        
        {/* Protected Routes */}
        <Route
          path="/templates"
          element={
            <PrivateRoute>
              <TemplateList />
            </PrivateRoute>
          }
        />
        
        {/* Admin Only Routes */}
        <Route
          path="/admin/templates"
          element={
            <PrivateRoute adminOnly>
              <AdminTemplateList />
            </PrivateRoute>
          }
        />
        <Route
          path="/admin/templates/create"
          element={
            <PrivateRoute adminOnly>
              <AdminTemplateCreate />
            </PrivateRoute>
          }
        />
      </Routes>
    </div>
  );
}

export default App;
