import "./featured.scss"
import { CircularProgressbar } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

export const Featured = () => {
  return (
      <div className="featured">
          
          {/* dont need top - could leave out */}
          <div className="top"></div>
          <div className="bottom">
              <div className="featuredChart">
                  {/* insert progress bar of metrics here, strokwwidth changes size of bars */}
                  <CircularProgressbar value={70} text={"70%"} strokeWidth={5} />
                  
              </div>
              <p className="title"> Deadline</p>

          </div>
    </div>
  )
}

export default Featured