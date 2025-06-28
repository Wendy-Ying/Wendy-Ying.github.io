---
title: "Robot Navigation in Complex Challenging Scenarios"
excerpt: "<img src='/images/video1.gif' width='75%'>"
collection: portfolio
---

An efficient localized obstacle avoidance planner is implemented for complex scenarios with dynamic obstacles and narrow passages in real-world scenes. The motion state of obstacles is accurately estimated based on DBSCAN clustering and filtering methods, and the future position of obstacles is predicted using GMM. Meanwhile, a robust global navigation is realized by constructing a global map based on FAST-LIO. The local obstacle avoider is realized based on NeuPAN algorithm, where the high-speed trajectory planning is realized based on point constraints, which ensures that the robot avoids obstacles quickly and accurately in the local environment.