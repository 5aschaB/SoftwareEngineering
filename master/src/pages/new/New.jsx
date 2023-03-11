import Navbar from "../../components/navbar/Navbar"
import Sidebar from "../../components/sidebar/Sidebar"
import "./new.scss"
import React from "react";
import { MDBBtn, MDBContainer, MDBRadio } from "mdb-react-ui-kit";
import Survey from '../../components/survey/Survey'


// Survey page to be clicked from sidebar 

export const New = () => {
    return (
      <div className="new">
          <Sidebar />
          <div className="newContainer">
                <Navbar />
                
              <div className="top">
                  <h1>Complete Survey</h1>
              </div>

                <div className="bottom">
            <div className="left">
              <h1>Well-being</h1>
              Do you feel physically well enough to work on the project?
            </div>
            <br></br>
                    <div className="right">
                        <div className="survey">
                            <Survey/>
                        </div>
            </div>
          </div>
          




           <div className="bottom">
            <div className="left">
              <h1>Team Size </h1>
              Do you feel the team is understaffed?
            </div>
            <br></br>
                    <div className="right">
                        <div className="survey">
                            <Survey/>
                        </div>
            </div>
          </div>
          




           <div className="bottom">
            <div className="left">
              <h1>Team Morale</h1>
              Do you feel satisfied working on your team?
            </div>
            <br></br>
                    <div className="right">
                        <div className="survey">
                            <Survey/>
                        </div>
            </div>
          </div>
        
        

          </div>
    </div>
  )
}


export default New