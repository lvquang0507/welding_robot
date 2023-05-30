function [theta1,theta2,theta3,theta4,theta5,theta6] = ik(x,y,z,roll,pitch,yaw)
%Inverse kinematics for 6DOFs arm
%   Detailed explanation goes here

syms theta1 theta2 theta3 theta4 theta5 theta6;

% Links values
alpha1 = -pi/2;
d1=445;
r1=150;
alpha2 = 0;
d2=-150;
r2=900;
alpha3=-pi/2;
d3=150;
r3=150;
alpha4 = pi/2;
d4=238+700;
r4=0;
alpha5=-pi/2;
d5=0;
r5=0;
alpha6 = 0;
d6=199;
r6=0;


T10 = dh_matrix(theta1,alpha1,d1,r1);
T21 = dh_matrix(theta2,alpha2,d2,r2);
T32 = dh_matrix(theta3-pi/2,alpha3,d3,r3); %Theta angle default is offset by -pi/2
T43 = dh_matrix(theta4,alpha4,d4,r4);
T54 = dh_matrix(theta5,alpha5,d5,r5);
T65 = dh_matrix(theta6,alpha6,d6,r6);

T_eef_base = T10*T21*T32*T43*T54*T65;
R = rpy(roll,pitch,yaw);

r1_eq = T_eef_base(1,1) == R(1,1);
r2_eq = T_eef_base(2,2) == R(2,2);
r3_eq = T_eef_base(3,3) == R(3,3);
x_eq = T_eef_base(1,4) == x;
y_eq = T_eef_base(2,4) == y;
z_eq = T_eef_base(3,4) == z;
S = vpasolve([r1_eq,r2_eq,r3_eq,x_eq,y_eq,z_eq],[theta1,theta2,theta3,theta4,theta5,theta6]);
solve_theta1 = double(S.theta1)
solve_theta2 = double(S.theta2)
solve_theta3 = double(S.theta3)
solve_theta4 = double(S.theta4)
solve_theta5 = double(S.theta5)
solve_theta6 = double(S.theta6)

theta1 = [0 solve_theta1];
theta2 = [0 solve_theta2];
theta3 = [0 solve_theta3];
theta4 = [0 solve_theta4];
theta5 = [0 solve_theta5];
theta6 = [0 solve_theta6];
end

