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
              How happy are you working on your project 
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
              How much does working on this project affect your personal time? 
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
              How stressed are you regarding this project? 
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
              How happy are you with your team?
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