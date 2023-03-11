import "./navbar.scss"; 
import SearchIcon from '@mui/icons-material/Search';
import DarkModeOutlinedIcon from '@mui/icons-material/DarkModeOutlined';
import ZoomInOutlinedIcon from '@mui/icons-material/ZoomInOutlined';
import Brightness6OutlinedIcon from '@mui/icons-material/Brightness6Outlined';
import { DarkModeContext } from "../../context/darkModeContext";
import { useContext } from "react";

export const Navbar = () => {
          const { dispatch } = useContext(DarkModeContext);

  return (
      <div className='navbar' >
          
          <div className="wrapper">
              <div className="search">
                  <input type="text" placeholder="Search..." />
                  <SearchIcon className="icon"/>
              </div>
              <div className="items">
                  <div className="item">
                      <DarkModeOutlinedIcon className="icon" onClick={()=>dispatch({type:"TOGGLE"})} />
                  </div>
                  <div className="item">
                      <ZoomInOutlinedIcon className="icon"/>
                  </div>
                  <div className="item">
                      
                    <div className="item">
                      <Brightness6OutlinedIcon className="icon" onClick={()=>dispatch({type:"LIGHT"})}/>
                  </div>
                  <div className="item"></div>
            <img
              src="https://images.pexels.com/photos/941693/pexels-photo-941693.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=500"
              alt=""
              className="avatar"
            />
          </div>
              </div>
        </div>
    </div>
  )
}


export default Navbar 



// DARK MODE 
// ZOOM IN (DISABLED) - FULL SCREEN 
