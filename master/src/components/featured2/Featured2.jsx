import "./featured2.scss"

import {
  CircularProgressbar,
  buildStyles
} from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

export const Featured2 = () => {
  return (
      <div className="featured">
          
          {/* dont need top - could leave out */}
          <div className="top"></div>
          <div className="bottom">
              <div className="featuredChart">
                  {/* insert progress bar of metrics here, strokwwidth changes size of bars */}
          <CircularProgressbar value={40} text={"40%"} strokeWidth={10} styles={buildStyles({
          textColor: "grey",
          pathColor: "#fc4a28",

        })}  />
                  
              </div>
              <p className="title"> Budget</p>
          </div>
    </div>
  )
}

export default Featured2