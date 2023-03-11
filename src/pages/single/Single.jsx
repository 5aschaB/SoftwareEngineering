import React from 'react'
import Navbar from "../../components/navbar/Navbar"
import Sidebar from "../../components/sidebar/Sidebar"
import Table from "../../components/table/Table";
import "./single.scss"

const Single = () => {
  return (
      <div className='project'>
          
          <Sidebar />
          <div className="projectContainer">
              <Navbar />
              <Table></Table>
                <div className="bottom">
              * Risk is measured on a scale of 1-5. <b> (1 = most risky, 5 = least risky). </b> 
          </div>
          </div>
        
      </div>
  )
}

export default Single