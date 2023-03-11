import "./list.scss"
import Sidebar from "../../components/sidebar/Sidebar"
import Navbar from "../../components/navbar/Navbar"
import ChatBot from 'react-simple-chatbot';
import { Segment } from 'semantic-ui-react';
import { ThemeProvider } from 'styled-components';
import React from "react";



const List = () => {

const theme = {
  background: '#f5f8fb',
  fontFamily: 'Helvetica Neue',
  headerBgColor: '#fc4a28',
  headerFontColor: '#fff',
  headerFontSize: '15px',
  botBubbleColor: '#EF6C00',
  botFontColor: '#fff',
  userBubbleColor: '#fff',
  userFontColor: '#4a4a4a',
};

    const steps = [
    {
      id: "Greet",
      message: "Hello, How can I help you",
      trigger: "Done",
    },
    {
      id: "Done",
      message: "Please enter your name!",
      trigger: "waiting1",
      },
    
    {
      id: "waiting1",
      user: true,
      trigger: "Name",
      },
    
    {
      id: "Name",
      message: "Hi {previousValue}, Please select your issue",
      trigger: "issues",
      },
    
    {
      id: "issues",
      options: [
        {
          value: "Budget",
          label: "Budget",
          trigger: "Rating2",
        },
        {
          value: "Deadline",
          label: "Deadline",
          trigger: "Rating"
        },

      ],

      },
      {
        id: "Rating",
          message: "Rate the severity of this issue 1-5 (5 being high severity).",
          trigger: "waiting2"
      
      },
       {
      id: "waiting2",
      user: true,
      trigger: "Deadline",
      },

            {
        id: "Rating2",
          message: "Rate the severity of this issue 1-5 (5 being high severity).",
          trigger: "waiting3"
      
      },
       {
      id: "waiting3",
      user: true,
      trigger: "Budget",
      },
    
    {
      id: "Budget",
      message:
        "Thanks for letting your budget issue of rating: {previousValue}. Perhaps contact the financial advisor to further discuss this at 07123456789.",
      end: true,
    },
    {
      id: "Deadline",
      message:
        "Thanks for letting us know of your deadline issue of rating: {previousValue}. Here are some steps to help you: 1) revaluate your timeline 2) re-prioritise and re-delegate tasks 3)Communicate any changes with stakeholders",
      end: true,
    },
  ]; 

  return (
    <div className="list">
      <Sidebar />

      <div className="listContainer">
        <Navbar />
        
        <div className="chatbot">

          
          <ThemeProvider theme={theme}>
            <Segment>
              <ChatBot steps={steps} />
            </Segment>
          </ThemeProvider>
      </div>
    
      </div>
    </div>
  )
}

export default List