#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Empty.h>
#include <std_msgs/Float64.h>
#include <std_msgs/Int16.h>
#include <math.h>
ros::NodeHandle nh;
std_msgs::Empty motor_stop_msg;
//std_msgs::Int32 amnt_steps_msg;
std_msgs::String str_msg;
ros::Publisher pub_motor_stop("motor_stop", &motor_stop_msg);
ros::Publisher pub_chatter("chatter", &str_msg);
//ros::Publisher pub_temp("temperature", &temp_data);
void cb_parse(const std_msgs::Int16& cmd_msg);
ros::Subscriber<std_msgs::Int16> sub("cmd_steps", &cb_parse);
volatile uint16_t counterx=0;
volatile uint16_t stepperx=0; 
String Input;
void setup() {
  nh.initNode();
  nh.advertise(pub_motor_stop);
  nh.advertise(pub_chatter);
  //nh.advertise(pub_temp);
  nh.subscribe(sub);
  Serial.begin(57600);
  str_msg.data = "Init done";
  pub_chatter.publish( &str_msg );
//  Serial.println("Successfully initialized");
  //Serial.setTimeout(50);//1ms- the higher it is the longer Serial.readString() takes
  pinMode(13, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(36,OUTPUT);//Direction Pin on Motor Driver
  pinMode(38,OUTPUT);//Enable Pin on Motor Driver
  digitalWrite(36,HIGH);//High means cw,Low means ccw
  digitalWrite(38,HIGH);//High means disable, Low means enable
  initialize();
  freq(30);//change speed of motor (lower=faster) (don't go below 15)
}
void loop() {
  nh.spinOnce();
  delay(10);
//  str_msg.data = "ping";
//  pub_chatter.publish( &str_msg );
}
void initialize(void)
{
  // PWM setup
  //x only or ocr0a is only enabled
  //max speed=3.9 Hz (OCR0A=10), min speed=0.15 Hz (OCR0A=255)
  //sets up pwm (pwm > delay because interrupts are needed and delays completely shut off micro-controller)
  TCCR0A=0x43; //8-bit timer set to fast pwm with only A active, for toggle on match (50% duty cycle), wgm on 111
  TCCR0B=0x0D; //clk prescaler @ clk/1024 
  OCR0A=0x0; //pin toggles on every match @ top
  OCR0B=0x0; //pin toggles on every match @ top
  //DDRC|=(1<<DDC7);//output pin
  //PORTC|=(1<<PORTC7);//high pin (cw direction)  //works in arduino
  //setup interrupts
  TIMSK0&=~(1<<OCIE0A);//for x interrupts
  //TIMSK0|=(1<<OCIE0B);//for y interrupts
  sei();
}
void cb_parse(const std_msgs::Int16& cmd_msg){
    int16_t amnt_steps = cmd_msg.data;
    if (amnt_steps < 0)
      stepf(abs(amnt_steps));
    else
      stepr(abs(amnt_steps));
}
void stepf(uint16_t stepsf)
{//step forward stepsf steps forward=cw
  off();
  digitalWrite(36,HIGH);//High means cw,Low means ccw
  digitalWrite(38,LOW);//High means disable, Low means enable
  stepperx=stepsf;
  counterx=0;
  TIMSK0|=(1<<OCIE0A);
//  Serial.println("StepF/n");
}
void stepr(uint16_t stepsr)
{//step reverse stepsr steps
  off();
  digitalWrite(36,LOW);//High means cw,Low means ccw
  digitalWrite(38,LOW);//High means disable, Low means enable
  stepperx=stepsr;
  counterx=0;
  TIMSK0|=(1<<OCIE0A);
//  Serial.println("StepR\n");
}
void errorfunc(void)
{
//  Serial.println("Error");
}
void off(void)
{
  digitalWrite(38,HIGH);//High means disable, Low means enable
  pub_motor_stop.publish(&motor_stop_msg);
//  Serial.println("Off");
}
void freq(uint8_t motFreq)
{
  OCR0A=motFreq;
}
ISR(TIMER0_COMPA_vect)
{
  counterx++; 
  //Serial.println(counterx);
//  count_msg.data = counterx;
//  numbers.publish( &count_msg );
  if(counterx>=(stepperx))
  {
    off();
    TIMSK0&=~(1<<OCIE0A);
  }
}
