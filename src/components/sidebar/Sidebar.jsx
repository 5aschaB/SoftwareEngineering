import "./sidebar.scss";
import DashboardIcon from '@mui/icons-material/Dashboard';
import LogoutIcon from '@mui/icons-material/Logout';

import SettingsOutlinedIcon from '@mui/icons-material/SettingsOutlined';
import ChatBubbleOutlineOutlinedIcon from '@mui/icons-material/ChatBubbleOutlineOutlined';
import AccountCircleOutlinedIcon from '@mui/icons-material/AccountCircleOutlined';
import PollOutlinedIcon from '@mui/icons-material/PollOutlined';
import AssignmentOutlinedIcon from '@mui/icons-material/AssignmentOutlined';
import {Link} from "react-router-dom"

export const Sidebar = () => {
  return (
      <div className='sidebar'>          
           
      <div className="top">
        <Link to="/" style={{textDecoration:"none"}}>
          <span className="logo"> lamabama </span>
          </Link>
          </div>
          <hr />
          <div className="center">
              <ul>
          <p className="title">MAIN</p>
          <Link to="/" style={{ textDecoration: "none" }}>
             <li> <DashboardIcon className="icon"/> <span>Dashboard</span></li>
                  </Link>
                 
          <li><AssignmentOutlinedIcon className="icon" /><span>Projects</span></li>
          <Link to="/survey" style={{ textDecoration: "none" }}>
                  <li><ChatBubbleOutlineOutlinedIcon className="icon" /><span>Chatbot</span></li>
          </Link>
                  <li><PollOutlinedIcon className="icon" /><span>Survey</span></li>
                  <p className="title">USER</p>
                  <li><SettingsOutlinedIcon className="icon"/><span>Settings</span></li>
                  <li><AccountCircleOutlinedIcon className="icon"/><span>Profile</span></li>
                  <li><LogoutIcon className="icon"/> <span>Logout</span></li>
                </ul>
          </div>

          <div className="bottom">
          
         <div className="colorOption"> </div>
          <div className="colorOption"> </div>
           <div className="colorOption"> </div>
          
          
          </div>
   
        </div>
  )
}

export default Sidebar
