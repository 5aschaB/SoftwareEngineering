import "./navbar.scss"; 
import SearchIcon from '@mui/icons-material/Search';
import DarkModeOutlinedIcon from '@mui/icons-material/DarkModeOutlined';
import ZoomInOutlinedIcon from '@mui/icons-material/ZoomInOutlined';
import PollOutlinedIcon from '@mui/icons-material/PollOutlined';

export const Navbar = () => {
  return (
      <div className='navbar' >
          
          <div className="wrapper">
              <div className="search">
                  <input type="text" placeholder="Search..." />
                  <SearchIcon className="icon"/>
              </div>
              <div className="items">
                  <div className="item">
                      <DarkModeOutlinedIcon className="icon"/>
                  </div>
                  <div className="item">
                      <ZoomInOutlinedIcon className="icon"/>
                  </div>

                  <div className="item">
                      <PollOutlinedIcon className="icon" />
                      {/* should be changed by backend to increment when survey needs to be completed */}
                      <div className="counter">1</div> 
                      
                  </div>
                  <div className="item">
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
