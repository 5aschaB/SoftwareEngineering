import React from 'react'
import Navbar from "../../components/navbar/Navbar"
import Sidebar from "../../components/sidebar/Sidebar"
import Table from "../../components/table/Table";

const Single = () => {
  return (
      <div className='project'>
          
          <Sidebar />
          <div className="projectContainer">
      
              <Navbar />
              
          </div>
      </div>
  )
}

export default Single