#include "Table.hh"

#ifndef __CINT__
	ClassImp(Table)
#endif

Table::Table(string name, int number) {

	tableName = name;
	tableNumber = number;

}

void Table::setName(string name) {

	tableName = name;

}

void Table::setNumber(int number) {

	tableNumber = number;

}

string Table::getName() {

	return tableName;

}

int Table::getNumber() {

	return tableNumber;

}

int Table::getNNuclides() {

	return Nuclides.size();

}

int Table::getNBeamStates() {

	return beamStates.size();

}

void Table::addBeamState(bool s) {

	beamStates.push_back(s);

}

void Table::addTimeStep(double tS) {

	timeSteps.push_back(tS);

}

int Table::addNuclide(Nuclide n) {

	Nuclides.push_back(n);

	return (Nuclides.size()-1);

}

Nuclide* Table::getNuclide(int i) {

	return &Nuclides.at(i);

}

int Table::findNuclide(string n) {

	int pos = -1;

	for (int i = 0; i < Nuclides.size(); i++) {

		if (Nuclides.at(i).getName() == n) {

			pos = i;
			break;

		}

	}

	return pos;

}

void Table::finalizeTable() {

	int max = getNBeamStates();

	for (int i=0; i < getNNuclides(); i++) {

		getNuclide(i)->trimActivity(max);

	}

}

vector<double> Table::getTimeSteps() {

	return timeSteps;

}

vector<bool> Table::getBeamStates() {

	return beamStates;

}

void Table::listNuclides() {

	for (int i=0; i < Nuclides.size(); i++) {

		cout << i << ": " << (Nuclides.at(i)).getName() << endl;
	}

}

void Table::listNuclides(string n) {

	string nuclideName;

	for (int i=0; i < Nuclides.size(); i++) {

		nuclideName = (Nuclides.at(i)).getName();

		if (nuclideName.find(n) != std::string::npos) {

			cout << i << ": " << nuclideName << endl;

		}

	}

}

void Table::calculateTotals() {

	

}

void Table::getMostActive() {}
void Table::getMostActive(int) {}
void Table::getMostActive(double) {}






