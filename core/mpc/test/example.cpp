#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include "emp-sh2pc/emp-sh2pc.h"
using namespace emp;
using namespace std;

#define DSIZE 10
#define DUMMY_INPUT_TEST
#define INTEGER_MODE



/*********************************************************
	The following implementation are the applications
	and computations of CryptoE Project
**********************************************************/

//-----< Laplace random noise generator >-----------------
void generateLaplaceNoise(int* laplaceNoiseVec, int NOISE_SIZE, double e){

	std::default_random_engine generator;
  	std::geometric_distribution<int> distribution(1-e);
	for (int i=0; i < NOISE_SIZE; i++){
		int tmp_u, tmp_v;
		tmp_u = distribution(generator);
		tmp_v = distribution(generator);
		laplaceNoiseVec[i] = tmp_u - tmp_v;
	}

	return;
}

//------<Test Fucntion for millionare >----------------
void test_millionare(int party, int number) {
	Integer a(32, number, ALICE);
	Integer b(32, number, BOB);

	cout << "ALICE Input:\t"<<a.reveal<int>()<<endl;
	cout << "BOB Input:\t"<<b.reveal<int>()<<endl;
	cout << "ALICE larger?\t"<< (a>b).reveal<bool>()<<endl;
}

//----- < Test Sort Function >--------------------------
void test_sort(int party) {
	int size = 10;
	Batcher batcher1, batcher2;
	Integer *A = new Integer[size];
	for(int i = 0; i < size; ++i) {
		batcher1.add<Integer>(32, rand()%1024);
		batcher2.add<Integer>(32, rand()%1024);
	}

	batcher1.make_semi_honest(ALICE);
	batcher2.make_semi_honest(BOB);

	for(int i = 0; i < size; ++i)
		A[i] = batcher1.next<Integer>() ^ batcher2.next<Integer>();

	sort(A, size);
	for(int i = 0; i < size; ++i)
		cout << A[i].reveal<string>()<<endl;
}

//------< Teststub Implementation of Heavy Hitter SMC >----------------
void get_topK(int party, int *Noise, int *MaskData, int DATA_SIZE, int K){
	Batcher ASMaskData; 
	Batcher CSPLpNoise; 
	Batcher ASNoise;

	//Setup Result Vector
	Integer *A = new Integer[DATA_SIZE];
	int lpNoise[DATA_SIZE];
	generateLaplaceNoise(lpNoise, DATA_SIZE, 0.4);

	//Generation of Lap Noise from CSP side
	for(int i = 0; i < DATA_SIZE; ++i) {
        ASMaskData.add<Integer>(32, MaskData[i]);
		ASNoise.add<Integer>(32, Noise[i]);
		CSPLpNoise.add<Integer>(32, lpNoise[i]);
    }	

	ASMaskData.make_semi_honest(BOB);
	CSPLpNoise.make_semi_honest(BOB);
	ASNoise.make_semi_honest(ALICE);

	if (party == ALICE)
		cout<<"[+] AS side initialization complete, start secure computation"<<endl;
	else	
		cout<<"[+] CSP side initialization complete, start secure computation"<<endl;

	for(int i = 0; i < DATA_SIZE; ++i)
        A[i] = ASMaskData.next<Integer>() - ASNoise.next<Integer>() + CSPLpNoise.next<Integer>();

	sort(A, DATA_SIZE);
	
	//Max Count Result Only Reveals to ALICE(AS) side.
	if (party == ALICE){
		cout<<"[+] AS Side: Secure Computation Complete, Showing Results:"<<endl;
		for(int i=0; i <K; i++)
			cout<<A[DATA_SIZE - 1 - i].reveal<string>(ALICE)<<" ,";
		cout<<endl;
	}
		
	else{
		cout<<"[+] CSP Side: Secure Computation Complete, Showing Results:"<<endl;
		for(int i=0; i <K; i++)
			cout<<A[DATA_SIZE - 1 - i].reveal<string>(ALICE)<<" ,";
		cout<<endl;
	}	
}

//------<  Implementation of CSP-AS SMC >----------------
void csp_as_noisemax(int party, int *Noise, int *MaskData, int *lpNoise, int DATA_SIZE){


	Batcher ASMaskData; 
	Batcher ASNoise;
	Batcher CSPLpNoise; 
	
	//Setup Result Vector
	Integer *A = new Integer[DATA_SIZE];
	
	//Initialize data structures for SMC protocol
	for(int i = 0; i < DATA_SIZE; ++i) {
        ASMaskData.add<Integer>(32, MaskData[i]);
        ASNoise.add<Integer>(32, Noise[i]);
		CSPLpNoise.add<Integer>(32, lpNoise[i]);
    }	

	ASMaskData.make_semi_honest(BOB);
	ASNoise.make_semi_honest(ALICE);
	CSPLpNoise.make_semi_honest(BOB);

	if (party == ALICE)
		cout<<"[+] AS side initialization complete, start secure computation"<<endl;
	else	
		cout<<"[+] CSP side initialization complete, start secure computation"<<endl;

	for(int i = 0; i < DATA_SIZE; ++i)
        A[i] = ASMaskData.next<Integer>() - ASNoise.next<Integer>() + CSPLpNoise.next<Integer>();

	sort(A, DATA_SIZE);
	
	//Max Count Result Only Reveals to ALICE(AS) side.
	if (party == ALICE)
		cout<<"[+] AS Side: Secure Computation Complete, Showing Results:"<<A[DATA_SIZE - 1].reveal<string>(ALICE)<<endl;
	else	
		cout<<"[+] CSP Side: Secure Computation Complete, Showing Results:"<<A[DATA_SIZE - 1].reveal<string>(ALICE)<<endl;
}

//------< Calculate the Distinct Number >----------------
void csp_as_distinct(int party, int *EncVec, int DATA_SIZE){

	Batcher CSPDecVec; 
	Batcher Pivot;
	
	//Integer Pivot(32, 0, ALICE);
	Integer *A = new Integer[DATA_SIZE];

	Integer One(32, 1, ALICE);
	Integer Zero(32, 0, ALICE);
	
	//Generation of Lap Noise from CSP side
	for(int i = 0; i < DATA_SIZE; ++i) {
        CSPDecVec.add<Integer>(32, EncVec[i]);
		Pivot.add<Integer>(32, 0);
    }	

	CSPDecVec.make_semi_honest(ALICE);

	if (party == ALICE)
		cout<<"[+] AS side initialization complete, start secure computation"<<endl;
	else	
		cout<<"[+] CSP side initialization complete, start secure computation"<<endl;

	// Bool Evaluation
	for(int i = 0; i < DATA_SIZE; ++i){
		if( (CSPDecVec.next<Integer>() > Pivot.next<Integer>()).reveal() )
			A[i] = One;
		else
			A[i] = Zero;
	}

	//Max Count Result Only Reveals to ALICE(AS) side.
	if (party == ALICE)
		cout<<"[+] AS Side: Secure Computation Complete, Showing Results:"<<A[DATA_SIZE - 1].reveal<string>(ALICE)<<endl;
	else	
		cout<<"[+] CSP Side: Secure Computation Complete, Showing Results:"<<A[DATA_SIZE - 1].reveal<string>(ALICE)<<endl;
}


#ifdef NOISEMAX_FLOAT
//------< Teststub Implementation of CSP-AS SMC in Float Input >----------------
void csp_as_noisemax_float(int party, float *Noise, float *MaskData, int DATA_SIZE){

	Batcher ASMaskData; 
	Batcher ASNoise;
	Batcher CSPLpNoise; 
	
	//Setup Result Vector
	Float a(24, 9, 0.0, ALICE);;
	
	//Generation of Lap Noise from CSP side
	for(int i = 0; i < DATA_SIZE; ++i) {
        ASMaskData.add<Float>(24, 9, MaskData[i]);
        ASNoise.add<Float>(24, 9, Noise[i]);
		CSPLpNoise.add<Float>(24, 9, Noise[i]);
    }	

	ASMaskData.make_semi_honest(BOB);
	ASNoise.make_semi_honest(ALICE);
	CSPLpNoise.make_semi_honest(BOB);

	if (party == ALICE)
		cout<<"[+] AS side initialization complete, start secure computation"<<endl;
	else	
		cout<<"[+] CSP side initialization complete, start secure computation"<<endl;
	
}
#endif

/*********************************************************
	Dispather
**********************************************************/

void test_noise_max(int party, int samplesize, string fn){

	// Create Dummy Array
	int DATA_SIZE = samplesize;
	int DUMMY[samplesize];
	for (int i = 0; i < samplesize; i++)
		DUMMY[i] = 0;


	if (party==BOB){
		int array_size = 0;
		vector <int> data;
		ifstream is(fn);
		int x;
		while (is >> x){
			data.push_back(x);
			array_size++;
		}

		if (samplesize > array_size)
			return;

		int MaskData[DATA_SIZE];
		for (int i = 0; i <DATA_SIZE; i++)
			MaskData[i] = data[i];

		//Generate LP Noise
		int lpNoise[DATA_SIZE];
		generateLaplaceNoise(lpNoise, DATA_SIZE, 0.4);
		csp_as_noisemax(party, DUMMY, MaskData, lpNoise, DATA_SIZE);
	}
	else if (party == ALICE){

		// ASside Noise
		vector <int> tmp;
		ifstream is2(fn);
		int y;
		while (is2 >> y){
			tmp.push_back(y);
		}
		int ASNoise[DATA_SIZE];
		for (int i = 0; i <DATA_SIZE; i++)
			ASNoise[i] = tmp[i];
		
		csp_as_noisemax(party, ASNoise, DUMMY, DUMMY, DATA_SIZE);
	}

}
//----------< Test Stub >---------------------------------
int main(int argc, char** argv) {

	int port, party;
	parse_party_and_port(argv, &party, &port);
	NetIO * io = new NetIO(party==ALICE ? nullptr : "127.0.0.1", port);
	setup_semi_honest(io, party);

	if (party==BOB)
		test_noise_max(party, 10, "as_noise_count.txt");
	else if (party==ALICE)
		test_noise_max(party, 10, "as_noise.txt");

	delete io;
}
