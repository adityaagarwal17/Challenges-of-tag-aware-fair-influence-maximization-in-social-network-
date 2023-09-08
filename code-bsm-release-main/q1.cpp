#include <bits/stdc++.h>
using namespace std;

void findAns(){
  int n,m,h;
  cin>>n>>m>>h;
  vector<vector<int>> arr(n,vector<int>(m));
  for(int i=0;i<n;i++){
    for(int j=0;j<m;j++){
    cin>>arr[i][j];
    }
  }
  sort(arr[0].begin(),arr[0].end());
  int pt=0;
  int penalty=0;
  int time=0;
  int rank=1;
  for(int i=0;i<arr[0].size();i++){
    time =time + arr[0][i];
    if(time<=h){
        pt++;
        penalty+=time;
    }
  }
  for(int i=1;i<n;i++){
    sort(arr[i].begin(),arr[i].end());
    int pt1=0;
    int penalty1=0;
    int time1=0;
    for(int j=0;j<m;j++){
        time1 =time1 + arr[i][j];
    if(time1<=h){
        pt1++;
        penalty1+=time;
    }
    }
    if(pt1 > pt){
        rank++;
    }
    else if(pt1==pt && penalty1 < penalty)[
        rank++;
    ]
  }
  cout<<rank<<endl;
}
int main(){
    int t;
    cin>>t;
    while (t!=0)
    {
        findAns();
        t--;
    }
    return 0;
}